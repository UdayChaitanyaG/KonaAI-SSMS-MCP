import { Tool } from '@modelcontextprotocol/sdk/types.js';
import { MasterDatabase } from '../database/master-db.js';
import { DataManagementDatabase } from '../database/data-mgmt-db.js';

export class SchemaTool {
  private masterDb: MasterDatabase;
  private dataMgmtDb: DataManagementDatabase;

  constructor(masterDb: MasterDatabase, dataMgmtDb: DataManagementDatabase) {
    this.masterDb = masterDb;
    this.dataMgmtDb = dataMgmtDb;
  }

  getSchemaTool(): Tool {
    return {
      name: 'getSchema',
      description: 'Get database schema information',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database to get schema for'
          },
          objectType: {
            type: 'string',
            enum: ['tables', 'procedures', 'triggers', 'views', 'all'],
            description: 'Type of database objects to retrieve',
            default: 'all'
          }
        },
        required: ['database']
      }
    };
  }

  getTablesTool(): Tool {
    return {
      name: 'getTables',
      description: 'Get list of tables in the database',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database to get tables from'
          }
        },
        required: ['database']
      }
    };
  }

  getTableSchemaTool(): Tool {
    return {
      name: 'getTableSchema',
      description: 'Get detailed schema for a specific table',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database containing the table'
          },
          tableName: {
            type: 'string',
            description: 'Name of the table'
          },
          schema: {
            type: 'string',
            description: 'Schema name (default: dbo)',
            default: 'dbo'
          }
        },
        required: ['database', 'tableName']
      }
    };
  }

  getStoredProceduresTool(): Tool {
    return {
      name: 'getStoredProcedures',
      description: 'Get list of stored procedures in the database',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database to get procedures from'
          }
        },
        required: ['database']
      }
    };
  }

  getTriggersTool(): Tool {
    return {
      name: 'getTriggers',
      description: 'Get list of triggers in the database',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database to get triggers from'
          }
        },
        required: ['database']
      }
    };
  }

  getViewsTool(): Tool {
    return {
      name: 'getViews',
      description: 'Get list of views in the database',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database to get views from'
          }
        },
        required: ['database']
      }
    };
  }

  async getSchema(args: { database: 'master' | 'datamgmt'; objectType?: string }): Promise<any> {
    const { database, objectType = 'all' } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      const result: any = {};
      
      if (objectType === 'all' || objectType === 'tables') {
        result.tables = await db.getTables();
      }
      
      if (objectType === 'all' || objectType === 'procedures') {
        result.procedures = await db.getStoredProcedures();
      }
      
      if (objectType === 'all' || objectType === 'triggers') {
        result.triggers = await db.getTriggers();
      }
      
      if (objectType === 'all' || objectType === 'views') {
        result.views = await db.getViews();
      }
      
      return {
        success: true,
        database: database,
        schema: result
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }

  async getTables(args: { database: 'master' | 'datamgmt' }): Promise<any> {
    const { database } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      const tables = await db.getTables();
      return {
        success: true,
        database: database,
        tables: tables
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }

  async getTableSchema(args: { 
    database: 'master' | 'datamgmt'; 
    tableName: string; 
    schema?: string 
  }): Promise<any> {
    const { database, tableName, schema = 'dbo' } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      const tableSchema = await db.getTableSchema(tableName, schema);
      return {
        success: true,
        database: database,
        table: `${schema}.${tableName}`,
        schema: tableSchema
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }

  async getStoredProcedures(args: { database: 'master' | 'datamgmt' }): Promise<any> {
    const { database } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      const procedures = await db.getStoredProcedures();
      return {
        success: true,
        database: database,
        procedures: procedures
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }

  async getTriggers(args: { database: 'master' | 'datamgmt' }): Promise<any> {
    const { database } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      const triggers = await db.getTriggers();
      return {
        success: true,
        database: database,
        triggers: triggers
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }

  async getViews(args: { database: 'master' | 'datamgmt' }): Promise<any> {
    const { database } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      const views = await db.getViews();
      return {
        success: true,
        database: database,
        views: views
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }
}
