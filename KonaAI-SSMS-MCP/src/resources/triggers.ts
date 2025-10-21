import { Resource } from '@modelcontextprotocol/sdk/types.js';
import { MasterDatabase } from '../database/master-db.js';
import { DataManagementDatabase } from '../database/data-mgmt-db.js';

export class TriggersResource {
  private masterDb: MasterDatabase;
  private dataMgmtDb: DataManagementDatabase;

  constructor(masterDb: MasterDatabase, dataMgmtDb: DataManagementDatabase) {
    this.masterDb = masterDb;
    this.dataMgmtDb = dataMgmtDb;
  }

  async listTriggers(database: 'master' | 'datamgmt'): Promise<Resource[]> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    const triggers = await db.getTriggers();
    
    return triggers.map(trigger => ({
      uri: `mcp://ssms/${database}/triggers/${trigger.trigger_name}`,
      name: trigger.trigger_name,
      description: `Trigger: ${trigger.trigger_name} on table ${trigger.table_name}`,
      mimeType: 'text/sql'
    }));
  }

  async getTriggerResource(uri: string): Promise<{ contents: Array<{ uri: string; mimeType: string; text: string }> }> {
    const parts = uri.split('/');
    const database = parts[2] as 'master' | 'datamgmt';
    const triggerName = parts[4];
    
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    // Get trigger definition
    const definition = await db.getTriggerDefinition(triggerName);
    
    return {
      contents: [{
        uri: uri,
        mimeType: 'text/sql',
        text: definition
      }]
    };
  }

  async getTriggerDefinition(database: 'master' | 'datamgmt', triggerName: string): Promise<string> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    return await db.getTriggerDefinition(triggerName);
  }

  async getTriggersForTable(database: 'master' | 'datamgmt', tableName: string): Promise<any[]> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    const triggers = await db.getTriggers();
    return triggers.filter(trigger => trigger.table_name === tableName);
  }
}
