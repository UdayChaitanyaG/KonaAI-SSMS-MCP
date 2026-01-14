"""
Base database connection class with pyodbc connection pooling and error handling.
"""

import logging
import time
from typing import Any, Dict, List, Optional, Union
from contextlib import contextmanager
import pyodbc
from pyodbc import Connection, Cursor

from config.database_config import DatabaseConfig, get_connection_string


logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    """Database connection related errors."""
    pass


class DatabaseQueryError(Exception):
    """Database query execution errors."""
    pass


class BaseDatabase:
    """
    Base database connection class with connection pooling and error handling.
    """
    
    def __init__(self, db_config: DatabaseConfig, max_connections: int = 10):
        """
        Initialize database connection.
        
        Args:
            db_config: Database configuration
            max_connections: Maximum number of connections in pool
        """
        self.db_config = db_config
        self.max_connections = max_connections
        self.connection_string = get_connection_string(db_config)
        self._connection_pool: List[Connection] = []
        self._pool_lock = False
        
    def _get_connection(self) -> Connection:
        """
        Get a connection from the pool or create a new one.
        
        Returns:
            Database connection
            
        Raises:
            DatabaseConnectionError: If connection cannot be established
        """
        try:
            # Try to get existing connection from pool
            if self._connection_pool:
                connection = self._connection_pool.pop()
                # Test if connection is still alive
                try:
                    connection.execute("SELECT 1")
                    return connection
                except pyodbc.Error:
                    # Connection is dead, close it and create new one
                    try:
                        connection.close()
                    except:
                        pass
            
            # Create new connection
            connection = pyodbc.connect(
                self.connection_string,
                timeout=self.db_config.timeout
            )
            connection.autocommit = True
            return connection
            
        except pyodbc.Error as e:
            error_msg = str(e)
            logger.error(f"Failed to connect to database: {e}")
            
            # Provide helpful error messages
            helpful_msg = f"Failed to connect to database: {error_msg}"
            
            # Add troubleshooting hints based on error
            if "53" in error_msg or "not found" in error_msg.lower() or "not accessible" in error_msg.lower():
                helpful_msg += (
                    f"\n\nTroubleshooting:\n"
                    f"1. Verify server name '{self.db_config.server}' is correct\n"
                    f"2. Check if SQL Server is running and accessible\n"
                    f"3. Verify network connectivity to the server\n"
                    f"4. Check if SQL Server allows remote connections\n"
                    f"5. Try different server name formats:\n"
                    f"   - IP address: 192.168.1.100\n"
                    f"   - Server name: SERVERNAME\n"
                    f"   - Named instance: SERVERNAME\\INSTANCENAME\n"
                    f"   - With port: SERVERNAME,1433\n"
                    f"6. Check firewall settings\n"
                    f"7. Verify SQL Server Browser service is running (for named instances)"
                )
            elif "login" in error_msg.lower() or "authentication" in error_msg.lower():
                helpful_msg += (
                    f"\n\nTroubleshooting:\n"
                    f"1. Verify username '{self.db_config.username}' is correct\n"
                    f"2. Verify password is correct\n"
                    f"3. Check if SQL Server Authentication is enabled\n"
                    f"4. Verify user has access to database '{self.db_config.database}'"
                )
            elif "timeout" in error_msg.lower():
                helpful_msg += (
                    f"\n\nTroubleshooting:\n"
                    f"1. Increase connection timeout (current: {self.db_config.timeout}s)\n"
                    f"2. Check network latency\n"
                    f"3. Verify SQL Server is responding\n"
                    f"4. Check firewall rules"
                )
            
            raise DatabaseConnectionError(helpful_msg)
    
    def _return_connection(self, connection: Connection):
        """
        Return connection to pool.
        
        Args:
            connection: Database connection to return
        """
        try:
            if len(self._connection_pool) < self.max_connections:
                self._connection_pool.append(connection)
            else:
                connection.close()
        except Exception as e:
            logger.warning(f"Error returning connection to pool: {e}")
            try:
                connection.close()
            except:
                pass
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            Database connection
        """
        connection = None
        try:
            connection = self._get_connection()
            yield connection
        except Exception as e:
            if connection:
                try:
                    connection.rollback()
                except:
                    pass
            raise
        finally:
            if connection:
                self._return_connection(connection)
    
    def execute_query(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None,
        fetch: bool = True
    ) -> Union[List[Dict[str, Any]], int]:
        """
        Execute a SQL query with parameters.
        
        Args:
            query: SQL query string
            parameters: Query parameters
            fetch: Whether to fetch results
            
        Returns:
            Query results or affected row count
            
        Raises:
            DatabaseQueryError: If query execution fails
        """
        start_time = time.time()
        
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                
                # Add parameters if provided
                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)
                
                if fetch:
                    # Fetch all results
                    columns = [column[0] for column in cursor.description] if cursor.description else []
                    rows = cursor.fetchall()
                    
                    # Convert to list of dictionaries
                    results = []
                    for row in rows:
                        row_dict = {}
                        for i, value in enumerate(row):
                            row_dict[columns[i]] = value
                        results.append(row_dict)
                    
                    execution_time = time.time() - start_time
                    logger.info(f"Query executed in {execution_time:.3f}s, returned {len(results)} rows")
                    return results
                else:
                    # Return affected row count
                    affected_rows = cursor.rowcount
                    execution_time = time.time() - start_time
                    logger.info(f"Query executed in {execution_time:.3f}s, affected {affected_rows} rows")
                    return affected_rows
                    
        except pyodbc.Error as e:
            logger.error(f"Database query error: {e}")
            raise DatabaseQueryError(f"Database query failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {e}")
            raise DatabaseQueryError(f"Unexpected error: {e}")
    
    def execute_procedure(
        self,
        procedure_name: str,
        parameters: Optional[Dict[str, Any]] = None,
        output_parameters: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute a stored procedure.
        
        Args:
            procedure_name: Name of the stored procedure
            parameters: Input parameters
            output_parameters: List of output parameter names
            
        Returns:
            Dictionary containing result sets and output parameters
            
        Raises:
            DatabaseQueryError: If procedure execution fails
        """
        start_time = time.time()
        
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                
                # Build procedure call
                if parameters:
                    param_placeholders = ", ".join([f"@{param}" for param in parameters.keys()])
                    call_query = f"EXEC {procedure_name} {param_placeholders}"
                    cursor.execute(call_query, parameters)
                else:
                    cursor.execute(f"EXEC {procedure_name}")
                
                # Fetch result sets
                result_sets = []
                while True:
                    try:
                        columns = [column[0] for column in cursor.description] if cursor.description else []
                        rows = cursor.fetchall()
                        
                        if not rows:
                            break
                            
                        # Convert to list of dictionaries
                        result_set = []
                        for row in rows:
                            row_dict = {}
                            for i, value in enumerate(row):
                                row_dict[columns[i]] = value
                            result_set.append(row_dict)
                        
                        result_sets.append(result_set)
                        
                        # Move to next result set
                        if not cursor.nextset():
                            break
                            
                    except pyodbc.Error:
                        # No more result sets
                        break
                
                # Get output parameters if specified
                output_values = {}
                if output_parameters:
                    for param_name in output_parameters:
                        try:
                            # Get output parameter value
                            output_cursor = connection.cursor()
                            output_cursor.execute(f"SELECT @{param_name}")
                            result = output_cursor.fetchone()
                            if result:
                                output_values[param_name] = result[0]
                        except pyodbc.Error as e:
                            logger.warning(f"Could not retrieve output parameter {param_name}: {e}")
                
                execution_time = time.time() - start_time
                logger.info(f"Procedure {procedure_name} executed in {execution_time:.3f}s")
                
                return {
                    "result_sets": result_sets,
                    "output_parameters": output_values,
                    "execution_time": execution_time
                }
                
        except pyodbc.Error as e:
            logger.error(f"Database procedure error: {e}")
            raise DatabaseQueryError(f"Stored procedure execution failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during procedure execution: {e}")
            raise DatabaseQueryError(f"Unexpected error: {e}")
    
    def begin_transaction(self) -> Connection:
        """
        Begin a new transaction.
        
        Returns:
            Connection with transaction started
        """
        connection = self._get_connection()
        connection.autocommit = False
        return connection
    
    def commit_transaction(self, connection: Connection):
        """
        Commit a transaction.
        
        Args:
            connection: Connection with transaction to commit
        """
        try:
            connection.commit()
        finally:
            connection.autocommit = True
            self._return_connection(connection)
    
    def rollback_transaction(self, connection: Connection):
        """
        Rollback a transaction.
        
        Args:
            connection: Connection with transaction to rollback
        """
        try:
            connection.rollback()
        finally:
            connection.autocommit = True
            self._return_connection(connection)
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result[0] == 1
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def close_all_connections(self):
        """Close all connections in the pool."""
        for connection in self._connection_pool:
            try:
                connection.close()
            except:
                pass
        self._connection_pool.clear()
    
    def __del__(self):
        """Cleanup connections on destruction."""
        self.close_all_connections()
