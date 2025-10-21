import { Resource } from '@modelcontextprotocol/sdk/types.js';
import { MasterDatabase } from '../database/master-db.js';
import { DataManagementDatabase } from '../database/data-mgmt-db.js';

export class TablesResource {
  private masterDb: MasterDatabase;
  private dataMgmtDb: DataManagementDatabase;

  constructor(masterDb: MasterDatabase, dataMgmtDb: DataManagementDatabase) {
    this.masterDb = masterDb;
    this.dataMgmtDb = dataMgmtDb;
  }

  async listTables(database: 'master' | 'datamgmt'): Promise<Resource[]> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    const tables = await db.getTables();
    
    return tables.map(table => ({
      uri: `mcp://ssms/${database}/tables/${table.table_schema}.${table.table_name}`,
      name: `${table.table_schema}.${table.table_name}`,
      description: `Table: ${table.table_schema}.${table.table_name}`,
      mimeType: 'application/json'
    }));
  }

  async getTableResource(uri: string): Promise<{ contents: Array<{ uri: string; mimeType: string; text: string }> }> {
    const parts = uri.split('/');
    const database = parts[2] as 'master' | 'datamgmt';
    const tableName = parts[4];
    
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    // Get table schema
    const schema = await db.getTableSchema(tableName);
    
    // Get sample data (first 10 rows)
    const data = await db.getTableData(tableName, 'dbo', 10, 0);
    
    const schemaText = JSON.stringify({
      table: tableName,
      schema: schema,
      sampleData: data
    }, null, 2);

    return {
      contents: [{
        uri: uri,
        mimeType: 'application/json',
        text: schemaText
      }]
    };
  }

  async getTableSchema(database: 'master' | 'datamgmt', tableName: string, schema: string = 'dbo'): Promise<any> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    return await db.getTableSchema(tableName, schema);
  }

  async getTableData(
    database: 'master' | 'datamgmt', 
    tableName: string, 
    schema: string = 'dbo',
    limit: number = 100,
    offset: number = 0
  ): Promise<any[]> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    return await db.getTableData(tableName, schema, limit, offset);
  }
}
