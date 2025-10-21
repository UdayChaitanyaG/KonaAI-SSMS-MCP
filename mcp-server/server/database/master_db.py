"""
Master database operations for KonaAI Master database.
"""

import logging
from typing import Any, Dict, List, Optional

from .base import BaseDatabase
from ..config import DatabaseConfig


logger = logging.getLogger(__name__)


class MasterDatabase(BaseDatabase):
    """
    Master database operations for KonaAI Master database.
    """
    
    def __init__(self, db_config: DatabaseConfig):
        """
        Initialize Master database connection.
        
        Args:
            db_config: Master database configuration
        """
        super().__init__(db_config)
        self.database_name = "Master"
    
    def get_tables(self) -> List[Dict[str, Any]]:
        """
        Get list of all tables in the Master database.
        
        Returns:
            List of table information dictionaries
        """
        query = """
            SELECT 
                TABLE_SCHEMA as table_schema,
                TABLE_NAME as table_name,
                TABLE_TYPE as table_type
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """
        return self.execute_query(query)
    
    def get_table_schema(self, table_name: str, schema: str = 'dbo') -> List[Dict[str, Any]]:
        """
        Get detailed schema information for a specific table.
        
        Args:
            table_name: Name of the table
            schema: Schema name (default: 'dbo')
            
        Returns:
            List of column information dictionaries
        """
        query = """
            SELECT 
                COLUMN_NAME as column_name,
                DATA_TYPE as data_type,
                IS_NULLABLE as is_nullable,
                COLUMN_DEFAULT as column_default,
                CHARACTER_MAXIMUM_LENGTH as character_maximum_length,
                NUMERIC_PRECISION as numeric_precision,
                NUMERIC_SCALE as numeric_scale,
                ORDINAL_POSITION as ordinal_position
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ? AND TABLE_SCHEMA = ?
            ORDER BY ORDINAL_POSITION
        """
        return self.execute_query(query, {'table_name': table_name, 'schema': schema})
    
    def get_primary_keys(self, table_name: str, schema: str = 'dbo') -> List[Dict[str, Any]]:
        """
        Get primary key information for a table.
        
        Args:
            table_name: Name of the table
            schema: Schema name (default: 'dbo')
            
        Returns:
            List of primary key information
        """
        query = """
            SELECT 
                kcu.COLUMN_NAME as column_name,
                kcu.ORDINAL_POSITION as ordinal_position
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu 
                ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
            WHERE tc.TABLE_NAME = ? 
                AND tc.TABLE_SCHEMA = ?
                AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
            ORDER BY kcu.ORDINAL_POSITION
        """
        return self.execute_query(query, {'table_name': table_name, 'schema': schema})
    
    def get_foreign_keys(self, table_name: str, schema: str = 'dbo') -> List[Dict[str, Any]]:
        """
        Get foreign key information for a table.
        
        Args:
            table_name: Name of the table
            schema: Schema name (default: 'dbo')
            
        Returns:
            List of foreign key information
        """
        query = """
            SELECT 
                fk.name as foreign_key_name,
                ccu.COLUMN_NAME as column_name,
                ccu2.TABLE_NAME as referenced_table_name,
                ccu2.COLUMN_NAME as referenced_column_name
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc 
                ON fk.object_id = fkc.constraint_object_id
            INNER JOIN sys.columns c 
                ON fkc.parent_object_id = c.object_id 
                AND fkc.parent_column_id = c.column_id
            INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu 
                ON ccu.COLUMN_NAME = c.name
            INNER JOIN sys.columns c2 
                ON fkc.referenced_object_id = c2.object_id 
                AND fkc.referenced_column_id = c2.column_id
            INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE ccu2 
                ON ccu2.COLUMN_NAME = c2.name
            WHERE ccu.TABLE_NAME = ? AND ccu.TABLE_SCHEMA = ?
        """
        return self.execute_query(query, {'table_name': table_name, 'schema': schema})
    
    def get_indexes(self, table_name: str, schema: str = 'dbo') -> List[Dict[str, Any]]:
        """
        Get index information for a table.
        
        Args:
            table_name: Name of the table
            schema: Schema name (default: 'dbo')
            
        Returns:
            List of index information
        """
        query = """
            SELECT 
                i.name as index_name,
                i.type_desc as index_type,
                i.is_unique as is_unique,
                i.is_primary_key as is_primary_key,
                c.name as column_name,
                ic.key_ordinal as key_ordinal
            FROM sys.indexes i
            INNER JOIN sys.index_columns ic 
                ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            INNER JOIN sys.columns c 
                ON ic.object_id = c.object_id AND ic.column_id = c.column_id
            INNER JOIN sys.tables t 
                ON i.object_id = t.object_id
            INNER JOIN sys.schemas s 
                ON t.schema_id = s.schema_id
            WHERE t.name = ? AND s.name = ?
            ORDER BY i.name, ic.key_ordinal
        """
        return self.execute_query(query, {'table_name': table_name, 'schema': schema})
    
    def get_stored_procedures(self) -> List[Dict[str, Any]]:
        """
        Get list of all stored procedures in the Master database.
        
        Returns:
            List of stored procedure information
        """
        query = """
            SELECT 
                ROUTINE_SCHEMA as routine_schema,
                ROUTINE_NAME as routine_name,
                ROUTINE_TYPE as routine_type,
                CREATED as created,
                LAST_ALTERED as last_altered
            FROM INFORMATION_SCHEMA.ROUTINES 
            WHERE ROUTINE_TYPE = 'PROCEDURE'
            ORDER BY ROUTINE_SCHEMA, ROUTINE_NAME
        """
        return self.execute_query(query)
    
    def get_stored_procedure_definition(self, procedure_name: str, schema: str = 'dbo') -> str:
        """
        Get the definition of a stored procedure.
        
        Args:
            procedure_name: Name of the stored procedure
            schema: Schema name (default: 'dbo')
            
        Returns:
            Stored procedure definition
        """
        query = """
            SELECT OBJECT_DEFINITION(OBJECT_ID(? + '.' + ?)) as definition
        """
        result = self.execute_query(query, {'schema': schema, 'procedure_name': procedure_name})
        return result[0]['definition'] if result else ''
    
    def get_stored_procedure_parameters(self, procedure_name: str, schema: str = 'dbo') -> List[Dict[str, Any]]:
        """
        Get parameter information for a stored procedure.
        
        Args:
            procedure_name: Name of the stored procedure
            schema: Schema name (default: 'dbo')
            
        Returns:
            List of parameter information
        """
        query = """
            SELECT 
                p.parameter_name,
                p.data_type,
                p.character_maximum_length,
                p.numeric_precision,
                p.numeric_scale,
                p.parameter_mode
            FROM INFORMATION_SCHEMA.PARAMETERS p
            WHERE p.specific_name = ? AND p.specific_schema = ?
            ORDER BY p.ordinal_position
        """
        return self.execute_query(query, {'procedure_name': procedure_name, 'schema': schema})
    
    def get_triggers(self) -> List[Dict[str, Any]]:
        """
        Get list of all triggers in the Master database.
        
        Returns:
            List of trigger information
        """
        query = """
            SELECT 
                t.name as trigger_name,
                OBJECT_NAME(t.parent_id) as table_name,
                SCHEMA_NAME(t.schema_id) as trigger_schema,
                t.is_disabled as is_disabled,
                t.is_not_for_replication as is_not_for_replication
            FROM sys.triggers t
            ORDER BY t.name
        """
        return self.execute_query(query)
    
    def get_trigger_definition(self, trigger_name: str) -> str:
        """
        Get the definition of a trigger.
        
        Args:
            trigger_name: Name of the trigger
            
        Returns:
            Trigger definition
        """
        query = """
            SELECT OBJECT_DEFINITION(OBJECT_ID(?)) as definition
        """
        result = self.execute_query(query, {'trigger_name': trigger_name})
        return result[0]['definition'] if result else ''
    
    def get_views(self) -> List[Dict[str, Any]]:
        """
        Get list of all views in the Master database.
        
        Returns:
            List of view information
        """
        query = """
            SELECT 
                TABLE_SCHEMA as table_schema,
                TABLE_NAME as table_name,
                VIEW_DEFINITION as view_definition
            FROM INFORMATION_SCHEMA.VIEWS 
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """
        return self.execute_query(query)
    
    def get_view_definition(self, view_name: str, schema: str = 'dbo') -> str:
        """
        Get the definition of a view.
        
        Args:
            view_name: Name of the view
            schema: Schema name (default: 'dbo')
            
        Returns:
            View definition
        """
        query = """
            SELECT OBJECT_DEFINITION(OBJECT_ID(? + '.' + ?)) as definition
        """
        result = self.execute_query(query, {'schema': schema, 'view_name': view_name})
        return result[0]['definition'] if result else ''
    
    def get_table_data(
        self, 
        table_name: str, 
        schema: str = 'dbo', 
        limit: int = 1000,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get data from a table with pagination.
        
        Args:
            table_name: Name of the table
            schema: Schema name (default: 'dbo')
            limit: Maximum number of rows to return
            offset: Number of rows to skip
            
        Returns:
            List of table data rows
        """
        query = f"""
            SELECT * FROM [{schema}].[{table_name}] 
            ORDER BY (SELECT NULL)
            OFFSET ? ROWS 
            FETCH NEXT ? ROWS ONLY
        """
        return self.execute_query(query, {'offset': offset, 'limit': limit})
    
    def get_table_row_count(self, table_name: str, schema: str = 'dbo') -> int:
        """
        Get the row count for a table.
        
        Args:
            table_name: Name of the table
            schema: Schema name (default: 'dbo')
            
        Returns:
            Number of rows in the table
        """
        query = f"SELECT COUNT(*) as row_count FROM [{schema}].[{table_name}]"
        result = self.execute_query(query)
        return result[0]['row_count'] if result else 0
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Get general database information.
        
        Returns:
            Dictionary with database information
        """
        query = """
            SELECT 
                DB_NAME() as database_name,
                @@VERSION as sql_server_version,
                GETDATE() as current_time
        """
        result = self.execute_query(query)
        return result[0] if result else {}
