#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// Import database connections
import { MasterDatabase } from './database/master-db.js';
import { DataManagementDatabase } from './database/data-mgmt-db.js';

// Import resources
import { TablesResource } from './resources/tables.js';
import { ProceduresResource } from './resources/procedures.js';
import { TriggersResource } from './resources/triggers.js';
import { ViewsResource } from './resources/views.js';

// Import tools
import { QueryTool } from './tools/query.js';
import { CrudTool } from './tools/crud.js';
import { SchemaTool } from './tools/schema.js';

class SSMSServer {
  private server: Server;
  private masterDb: MasterDatabase;
  private dataMgmtDb: DataManagementDatabase;
  
  // Resources
  private tablesResource: TablesResource;
  private proceduresResource: ProceduresResource;
  private triggersResource: TriggersResource;
  private viewsResource: ViewsResource;
  
  // Tools
  private queryTool: QueryTool;
  private crudTool: CrudTool;
  private schemaTool: SchemaTool;

  constructor() {
    this.server = new Server(
      {
        name: 'ssms-mcp-server',
        version: '1.0.0',
      }
    );

    // Initialize database connections
    this.masterDb = new MasterDatabase();
    this.dataMgmtDb = new DataManagementDatabase();

    // Initialize resources
    this.tablesResource = new TablesResource(this.masterDb, this.dataMgmtDb);
    this.proceduresResource = new ProceduresResource(this.masterDb, this.dataMgmtDb);
    this.triggersResource = new TriggersResource(this.masterDb, this.dataMgmtDb);
    this.viewsResource = new ViewsResource(this.masterDb, this.dataMgmtDb);

    // Initialize tools
    this.queryTool = new QueryTool(this.masterDb, this.dataMgmtDb);
    this.crudTool = new CrudTool(this.masterDb, this.dataMgmtDb);
    this.schemaTool = new SchemaTool(this.masterDb, this.dataMgmtDb);

    this.setupHandlers();
  }

  private setupHandlers() {
    // List resources handler
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      const resources = [];
      
      // Add table resources for both databases
      const masterTables = await this.tablesResource.listTables('master');
      const dataMgmtTables = await this.tablesResource.listTables('datamgmt');
      resources.push(...masterTables, ...dataMgmtTables);
      
      // Add procedure resources for both databases
      const masterProcedures = await this.proceduresResource.listProcedures('master');
      const dataMgmtProcedures = await this.proceduresResource.listProcedures('datamgmt');
      resources.push(...masterProcedures, ...dataMgmtProcedures);
      
      // Add trigger resources for both databases
      const masterTriggers = await this.triggersResource.listTriggers('master');
      const dataMgmtTriggers = await this.triggersResource.listTriggers('datamgmt');
      resources.push(...masterTriggers, ...dataMgmtTriggers);
      
      // Add view resources for both databases
      const masterViews = await this.viewsResource.listViews('master');
      const dataMgmtViews = await this.viewsResource.listViews('datamgmt');
      resources.push(...masterViews, ...dataMgmtViews);

      return { resources };
    });

    // Read resource handler
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;
      
      if (uri.includes('/tables/')) {
        return await this.tablesResource.getTableResource(uri);
      } else if (uri.includes('/procedures/')) {
        return await this.proceduresResource.getProcedureResource(uri);
      } else if (uri.includes('/triggers/')) {
        return await this.triggersResource.getTriggerResource(uri);
      } else if (uri.includes('/views/')) {
        return await this.viewsResource.getViewResource(uri);
      }
      
      throw new Error(`Unknown resource type: ${uri}`);
    });

    // List tools handler
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          this.queryTool.getTool(),
          this.crudTool.getInsertTool(),
          this.crudTool.getUpdateTool(),
          this.crudTool.getDeleteTool(),
          this.schemaTool.getSchemaTool(),
          this.schemaTool.getTablesTool(),
          this.schemaTool.getTableSchemaTool(),
          this.schemaTool.getStoredProceduresTool(),
          this.schemaTool.getTriggersTool(),
          this.schemaTool.getViewsTool(),
        ],
      };
    });

    // Call tool handler
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'executeQuery':
            return await this.queryTool.execute(args as any);
          
          case 'insertData':
            return await this.crudTool.insert(args as any);
          
          case 'updateData':
            return await this.crudTool.update(args as any);
          
          case 'deleteData':
            return await this.crudTool.delete(args as any);
          
          case 'getSchema':
            return await this.schemaTool.getSchema(args as any);
          
          case 'getTables':
            return await this.schemaTool.getTables(args as any);
          
          case 'getTableSchema':
            return await this.schemaTool.getTableSchema(args as any);
          
          case 'getStoredProcedures':
            return await this.schemaTool.getStoredProcedures(args as any);
          
          case 'getTriggers':
            return await this.schemaTool.getTriggers(args as any);
          
          case 'getViews':
            return await this.schemaTool.getViews(args as any);
          
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error occurred',
        };
      }
    });
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('SSMS MCP Server started');
  }
}

// Start the server
const server = new SSMSServer();
server.start().catch((error) => {
  console.error('Failed to start server:', error);
  process.exit(1);
});
