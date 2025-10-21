import sql from 'mssql';
import { config } from '../config.js';

export class DataManagementDatabase {
  private pool: sql.ConnectionPool | null = null;

  async connect(): Promise<void> {
    if (!this.pool) {
      this.pool = new sql.ConnectionPool(config.dataMgmtDb);
      await this.pool.connect();
    }
  }

  async disconnect(): Promise<void> {
    if (this.pool) {
      await this.pool.close();
      this.pool = null;
    }
  }

  async executeQuery<T = any>(query: string, parameters?: Record<string, any>): Promise<T[]> {
    await this.connect();
    
    if (!this.pool) {
      throw new Error('Database connection not established');
    }

    const request = this.pool.request();
    
    // Add parameters if provided
    if (parameters) {
      Object.entries(parameters).forEach(([key, value]) => {
        request.input(key, value);
      });
    }

    const result = await request.query(query);
    return result.recordset;
  }

  async executeProcedure<T = any>(
    procedureName: string, 
    parameters?: Record<string, any>
  ): Promise<T[]> {
    await this.connect();
    
    if (!this.pool) {
      throw new Error('Database connection not established');
    }

    const request = this.pool.request();
    
    // Add parameters if provided
    if (parameters) {
      Object.entries(parameters).forEach(([key, value]) => {
        request.input(key, value);
      });
    }

    const result = await request.execute(procedureName);
    return result.recordset;
  }

  async getTables(): Promise<Array<{ table_name: string; table_schema: string }>> {
    const query = `
      SELECT 
        TABLE_SCHEMA as table_schema,
        TABLE_NAME as table_name
      FROM INFORMATION_SCHEMA.TABLES 
      WHERE TABLE_TYPE = 'BASE TABLE'
      ORDER BY TABLE_SCHEMA, TABLE_NAME
    `;
    return this.executeQuery(query);
  }

  async getTableSchema(tableName: string, schema: string = 'dbo'): Promise<Array<{
    column_name: string;
    data_type: string;
    is_nullable: string;
    column_default: string;
    character_maximum_length: number;
  }>> {
    const query = `
      SELECT 
        COLUMN_NAME as column_name,
        DATA_TYPE as data_type,
        IS_NULLABLE as is_nullable,
        COLUMN_DEFAULT as column_default,
        CHARACTER_MAXIMUM_LENGTH as character_maximum_length
      FROM INFORMATION_SCHEMA.COLUMNS 
      WHERE TABLE_NAME = @tableName AND TABLE_SCHEMA = @schema
      ORDER BY ORDINAL_POSITION
    `;
    return this.executeQuery(query, { tableName, schema });
  }

  async getStoredProcedures(): Promise<Array<{ routine_name: string; routine_schema: string }>> {
    const query = `
      SELECT 
        ROUTINE_SCHEMA as routine_schema,
        ROUTINE_NAME as routine_name
      FROM INFORMATION_SCHEMA.ROUTINES 
      WHERE ROUTINE_TYPE = 'PROCEDURE'
      ORDER BY ROUTINE_SCHEMA, ROUTINE_NAME
    `;
    return this.executeQuery(query);
  }

  async getStoredProcedureDefinition(procedureName: string, schema: string = 'dbo'): Promise<string> {
    const query = `
      SELECT OBJECT_DEFINITION(OBJECT_ID(@schema + '.' + @procedureName)) as definition
    `;
    const result = await this.executeQuery<{ definition: string }>(query, { schema, procedureName });
    return result[0]?.definition || '';
  }

  async getTriggers(): Promise<Array<{ trigger_name: string; table_name: string; trigger_schema: string }>> {
    const query = `
      SELECT 
        t.name as trigger_name,
        OBJECT_NAME(t.parent_id) as table_name,
        SCHEMA_NAME(t.schema_id) as trigger_schema
      FROM sys.triggers t
      WHERE t.is_disabled = 0
      ORDER BY t.name
    `;
    return this.executeQuery(query);
  }

  async getTriggerDefinition(triggerName: string): Promise<string> {
    const query = `
      SELECT OBJECT_DEFINITION(OBJECT_ID(@triggerName)) as definition
    `;
    const result = await this.executeQuery<{ definition: string }>(query, { triggerName });
    return result[0]?.definition || '';
  }

  async getViews(): Promise<Array<{ table_name: string; table_schema: string }>> {
    const query = `
      SELECT 
        TABLE_SCHEMA as table_schema,
        TABLE_NAME as table_name
      FROM INFORMATION_SCHEMA.VIEWS 
      ORDER BY TABLE_SCHEMA, TABLE_NAME
    `;
    return this.executeQuery(query);
  }

  async getViewDefinition(viewName: string, schema: string = 'dbo'): Promise<string> {
    const query = `
      SELECT OBJECT_DEFINITION(OBJECT_ID(@schema + '.' + @viewName)) as definition
    `;
    const result = await this.executeQuery<{ definition: string }>(query, { schema, viewName });
    return result[0]?.definition || '';
  }

  async getTableData(
    tableName: string, 
    schema: string = 'dbo', 
    limit: number = config.maxRows,
    offset: number = 0
  ): Promise<any[]> {
    const query = `
      SELECT * FROM [${schema}].[${tableName}] 
      ORDER BY (SELECT NULL)
      OFFSET @offset ROWS 
      FETCH NEXT @limit ROWS ONLY
    `;
    return this.executeQuery(query, { limit, offset });
  }

  async insertData(
    tableName: string, 
    schema: string = 'dbo', 
    data: Record<string, any>
  ): Promise<number> {
    const columns = Object.keys(data).join(', ');
    const values = Object.keys(data).map(key => `@${key}`).join(', ');
    const parameters = Object.fromEntries(
      Object.entries(data).map(([key, value]) => [`${key}`, value])
    );

    const query = `
      INSERT INTO [${schema}].[${tableName}] (${columns}) 
      VALUES (${values})
    `;
    
    const result = await this.executeQuery(query, parameters);
    return 1; // Return affected rows count
  }

  async updateData(
    tableName: string,
    schema: string = 'dbo',
    data: Record<string, any>,
    whereClause: string,
    whereParameters: Record<string, any> = {}
  ): Promise<number> {
    const setClause = Object.keys(data).map(key => `[${key}] = @${key}`).join(', ');
    const parameters = { ...data, ...whereParameters };

    const query = `
      UPDATE [${schema}].[${tableName}] 
      SET ${setClause} 
      WHERE ${whereClause}
    `;
    
    await this.executeQuery(query, parameters);
    return 1; // Return affected rows count
  }

  async deleteData(
    tableName: string,
    schema: string = 'dbo',
    whereClause: string,
    whereParameters: Record<string, any> = {}
  ): Promise<number> {
    const query = `
      DELETE FROM [${schema}].[${tableName}] 
      WHERE ${whereClause}
    `;
    
    await this.executeQuery(query, whereParameters);
    return 1; // Return affected rows count
  }
}
