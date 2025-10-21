import { Resource } from '@modelcontextprotocol/sdk/types.js';
import { MasterDatabase } from '../database/master-db.js';
import { DataManagementDatabase } from '../database/data-mgmt-db.js';

export class ViewsResource {
  private masterDb: MasterDatabase;
  private dataMgmtDb: DataManagementDatabase;

  constructor(masterDb: MasterDatabase, dataMgmtDb: DataManagementDatabase) {
    this.masterDb = masterDb;
    this.dataMgmtDb = dataMgmtDb;
  }

  async listViews(database: 'master' | 'datamgmt'): Promise<Resource[]> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    const views = await db.getViews();
    
    return views.map(view => ({
      uri: `mcp://ssms/${database}/views/${view.table_schema}.${view.table_name}`,
      name: `${view.table_schema}.${view.table_name}`,
      description: `View: ${view.table_schema}.${view.table_name}`,
      mimeType: 'text/sql'
    }));
  }

  async getViewResource(uri: string): Promise<{ contents: Array<{ uri: string; mimeType: string; text: string }> }> {
    const parts = uri.split('/');
    const database = parts[2] as 'master' | 'datamgmt';
    const viewName = parts[4];
    
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    // Get view definition
    const definition = await db.getViewDefinition(viewName);
    
    return {
      contents: [{
        uri: uri,
        mimeType: 'text/sql',
        text: definition
      }]
    };
  }

  async getViewDefinition(database: 'master' | 'datamgmt', viewName: string, schema: string = 'dbo'): Promise<string> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    return await db.getViewDefinition(viewName, schema);
  }

  async queryView(
    database: 'master' | 'datamgmt', 
    viewName: string, 
    schema: string = 'dbo',
    limit: number = 100,
    offset: number = 0
  ): Promise<any[]> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    return await db.getTableData(viewName, schema, limit, offset);
  }
}
