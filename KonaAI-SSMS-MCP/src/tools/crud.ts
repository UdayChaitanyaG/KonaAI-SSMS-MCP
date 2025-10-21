import { Tool } from '@modelcontextprotocol/sdk/types.js';
import { MasterDatabase } from '../database/master-db.js';
import { DataManagementDatabase } from '../database/data-mgmt-db.js';

export class CrudTool {
  private masterDb: MasterDatabase;
  private dataMgmtDb: DataManagementDatabase;

  constructor(masterDb: MasterDatabase, dataMgmtDb: DataManagementDatabase) {
    this.masterDb = masterDb;
    this.dataMgmtDb = dataMgmtDb;
  }

  getInsertTool(): Tool {
    return {
      name: 'insertData',
      description: 'Insert data into a table',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database to insert into'
          },
          tableName: {
            type: 'string',
            description: 'Name of the table'
          },
          schema: {
            type: 'string',
            description: 'Schema name (default: dbo)',
            default: 'dbo'
          },
          data: {
            type: 'object',
            description: 'Data to insert',
            additionalProperties: true
          }
        },
        required: ['database', 'tableName', 'data']
      }
    };
  }

  getUpdateTool(): Tool {
    return {
      name: 'updateData',
      description: 'Update data in a table',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database to update'
          },
          tableName: {
            type: 'string',
            description: 'Name of the table'
          },
          schema: {
            type: 'string',
            description: 'Schema name (default: dbo)',
            default: 'dbo'
          },
          data: {
            type: 'object',
            description: 'Data to update',
            additionalProperties: true
          },
          whereClause: {
            type: 'string',
            description: 'WHERE clause for the update'
          },
          whereParameters: {
            type: 'object',
            description: 'Parameters for the WHERE clause',
            additionalProperties: true
          }
        },
        required: ['database', 'tableName', 'data', 'whereClause']
      }
    };
  }

  getDeleteTool(): Tool {
    return {
      name: 'deleteData',
      description: 'Delete data from a table',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database to delete from'
          },
          tableName: {
            type: 'string',
            description: 'Name of the table'
          },
          schema: {
            type: 'string',
            description: 'Schema name (default: dbo)',
            default: 'dbo'
          },
          whereClause: {
            type: 'string',
            description: 'WHERE clause for the delete'
          },
          whereParameters: {
            type: 'object',
            description: 'Parameters for the WHERE clause',
            additionalProperties: true
          }
        },
        required: ['database', 'tableName', 'whereClause']
      }
    };
  }

  async insert(args: { 
    database: 'master' | 'datamgmt'; 
    tableName: string; 
    schema?: string; 
    data: Record<string, any> 
  }): Promise<any> {
    const { database, tableName, schema = 'dbo', data } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      const result = await db.insertData(tableName, schema, data);
      return {
        success: true,
        affectedRows: result,
        message: `Successfully inserted data into ${schema}.${tableName}`
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }

  async update(args: { 
    database: 'master' | 'datamgmt'; 
    tableName: string; 
    schema?: string; 
    data: Record<string, any>; 
    whereClause: string; 
    whereParameters?: Record<string, any> 
  }): Promise<any> {
    const { database, tableName, schema = 'dbo', data, whereClause, whereParameters = {} } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      const result = await db.updateData(tableName, schema, data, whereClause, whereParameters);
      return {
        success: true,
        affectedRows: result,
        message: `Successfully updated data in ${schema}.${tableName}`
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }

  async delete(args: { 
    database: 'master' | 'datamgmt'; 
    tableName: string; 
    schema?: string; 
    whereClause: string; 
    whereParameters?: Record<string, any> 
  }): Promise<any> {
    const { database, tableName, schema = 'dbo', whereClause, whereParameters = {} } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      const result = await db.deleteData(tableName, schema, whereClause, whereParameters);
      return {
        success: true,
        affectedRows: result,
        message: `Successfully deleted data from ${schema}.${tableName}`
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }
}
