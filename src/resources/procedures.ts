import { Resource } from '@modelcontextprotocol/sdk/types.js';
import { MasterDatabase } from '../database/master-db.js';
import { DataManagementDatabase } from '../database/data-mgmt-db.js';

export class ProceduresResource {
  private masterDb: MasterDatabase;
  private dataMgmtDb: DataManagementDatabase;

  constructor(masterDb: MasterDatabase, dataMgmtDb: DataManagementDatabase) {
    this.masterDb = masterDb;
    this.dataMgmtDb = dataMgmtDb;
  }

  async listProcedures(database: 'master' | 'datamgmt'): Promise<Resource[]> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    const procedures = await db.getStoredProcedures();
    
    return procedures.map(proc => ({
      uri: `mcp://ssms/${database}/procedures/${proc.routine_schema}.${proc.routine_name}`,
      name: `${proc.routine_schema}.${proc.routine_name}`,
      description: `Stored Procedure: ${proc.routine_schema}.${proc.routine_name}`,
      mimeType: 'text/sql'
    }));
  }

  async getProcedureResource(uri: string): Promise<{ contents: Array<{ uri: string; mimeType: string; text: string }> }> {
    const parts = uri.split('/');
    const database = parts[2] as 'master' | 'datamgmt';
    const procedureName = parts[4];
    
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    
    // Get procedure definition
    const definition = await db.getStoredProcedureDefinition(procedureName);
    
    return {
      contents: [{
        uri: uri,
        mimeType: 'text/sql',
        text: definition
      }]
    };
  }

  async getProcedureDefinition(database: 'master' | 'datamgmt', procedureName: string, schema: string = 'dbo'): Promise<string> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    return await db.getStoredProcedureDefinition(procedureName, schema);
  }

  async executeProcedure(
    database: 'master' | 'datamgmt', 
    procedureName: string, 
    parameters: Record<string, any> = {},
    schema: string = 'dbo'
  ): Promise<any[]> {
    const db = database === 'master' ? this.masterDb : this.dataMgmtDb;
    const fullProcedureName = `${schema}.${procedureName}`;
    return await db.executeProcedure(fullProcedureName, parameters);
  }
}
