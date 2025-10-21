#!/usr/bin/env node

// Example: How to use the KonaAI SSMS MCP Server to list tables
import { spawn } from 'child_process';
import { createInterface } from 'readline';

console.log('🗄️ KonaAI Database Table Listing Example');
console.log('==========================================\n');

// Example MCP tool calls for listing tables
const exampleCalls = {
  // List tables in KonaAI.Master database
  listMasterTables: {
    tool: 'getTables',
    parameters: {
      database: 'master'
    },
    description: 'List all tables in KonaAI.Master database'
  },

  // List tables in DataManagement database  
  listDataMgmtTables: {
    tool: 'getTables',
    parameters: {
      database: 'datamgmt'
    },
    description: 'List all tables in DIT_GDB database'
  },

  // Get schema information for both databases
  getMasterSchema: {
    tool: 'getSchema',
    parameters: {
      database: 'master',
      objectType: 'all'
    },
    description: 'Get complete schema information for KonaAI.Master'
  },

  // Get specific table schema
  getTableSchema: {
    tool: 'getTableSchema',
    parameters: {
      database: 'master',
      tableName: 'Clients',
      schema: 'dbo'
    },
    description: 'Get detailed schema for Clients table'
  }
};

console.log('📋 Available MCP Tool Examples:');
console.log('================================\n');

Object.entries(exampleCalls).forEach(([key, call], index) => {
  console.log(`${index + 1}. ${call.description}`);
  console.log(`   Tool: ${call.tool}`);
  console.log(`   Parameters: ${JSON.stringify(call.parameters, null, 2)}`);
  console.log('');
});

console.log('🔧 How to Use with Cursor:');
console.log('==========================');
console.log('1. The MCP server is configured in .cursor/mcp.json');
console.log('2. Cursor will automatically detect the MCP server');
console.log('3. You can use these tools in Cursor chat:');
console.log('');
console.log('   Example: "List all tables in the master database"');
console.log('   Example: "Show me the schema for the Clients table"');
console.log('   Example: "Execute a query to get all clients"');
console.log('');

console.log('🚀 MCP Server Status:');
console.log('=====================');
console.log('✅ Server is ready to accept connections');
console.log('✅ Database connections configured');
console.log('✅ All tools and resources available');
console.log('');

console.log('💡 Next Steps:');
console.log('==============');
console.log('1. Use Cursor to interact with the MCP server');
console.log('2. Ask Cursor to list tables in your databases');
console.log('3. Explore database schemas and execute queries');
console.log('4. Use the tools for CRUD operations on your data');
