import { Tool } from '@modelcontextprotocol/sdk/types.js';
import { MasterDatabase } from '../database/master-db.js';
import { DataManagementDatabase } from '../database/data-mgmt-db.js';

export class QueryTool {
  private masterDb: MasterDatabase;
  private dataMgmtDb: DataManagementDatabase;

  constructor(masterDb: MasterDatabase, dataMgmtDb: DataManagementDatabase) {
    this.masterDb = masterDb;
    this.dataMgmtDb = dataMgmtDb;
  }

  getTool(): Tool {
    return {
      name: 'executeQuery',
      description: 'Execute SQL queries on the specified database',
      inputSchema: {
        type: 'object',
        properties: {
          database: {
            type: 'string',
            enum: ['master', 'datamgmt'],
            description: 'Database to execute query on'
          },
          query: {
            type: 'string',
            description: 'SQL query to execute'
          },
          parameters: {
            type: 'object',
            description: 'Query parameters (optional)',
            additionalProperties: true
          }
        },
        required: ['database', 'query']
      }
    };
  }

  async execute(args: { database: 'master' | 'datamgmt'; query: string; parameters?: Record<string, any> }): Promise<any> {
    const { database, query, parameters } = args;
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    try {
      // Basic SQL injection protection - only allow SELECT, INSERT, UPDATE, DELETE statements
      const trimmedQuery = query.trim().toLowerCase();
      if (!trimmedQuery.startsWith('select') && 
          !trimmedQuery.startsWith('insert') && 
          !trimmedQuery.startsWith('update') && 
          !trimmedQuery.startsWith('delete') &&
          !trimmedQuery.startsWith('exec') &&
          !trimmedQuery.startsWith('execute')) {
        throw new Error('Only SELECT, INSERT, UPDATE, DELETE, and EXEC statements are allowed');
      }

      const result = await db.executeQuery(query, parameters);
      return {
        success: true,
        data: result,
        rowCount: result.length
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }
}
