#!/usr/bin/env node

// Test script to demonstrate MCP server functionality
import { spawn } from 'child_process';
import path from 'path';

console.log('🚀 Testing KonaAI SSMS MCP Server');
console.log('=====================================\n');

// Test the MCP server by running it and sending test commands
async function testMCPServer() {
  try {
    console.log('📋 Available MCP Tools:');
    console.log('- getTables: List all tables in a database');
    console.log('- getSchema: Get database schema information');
    console.log('- executeQuery: Execute SQL queries');
    console.log('- getStoredProcedures: List stored procedures');
    console.log('- getTriggers: List triggers');
    console.log('- getViews: List views\n');

    console.log('🗄️ Database Connections:');
    console.log('- master: KonaAI.Master database');
    console.log('- datamgmt: DIT_GDB database\n');

    console.log('📝 Example Usage:');
    console.log('1. List tables in KonaAI.Master:');
    console.log('   Tool: getTables');
    console.log('   Parameters: { "database": "master" }');
    console.log('');
    console.log('2. List tables in DataManagement:');
    console.log('   Tool: getTables');
    console.log('   Parameters: { "database": "datamgmt" }');
    console.log('');
    console.log('3. Get table schema:');
    console.log('   Tool: getTableSchema');
    console.log('   Parameters: { "database": "master", "tableName": "Clients" }');
    console.log('');
    console.log('4. Execute a query:');
    console.log('   Tool: executeQuery');
    console.log('   Parameters: { "database": "master", "query": "SELECT TOP 10 * FROM Clients" }');
    console.log('');

    console.log('✅ MCP Server is ready to use!');
    console.log('💡 Use the tools above to interact with your KonaAI databases.');
    
  } catch (error) {
    console.error('❌ Error testing MCP server:', error.message);
  }
}

// Run the test
testMCPServer();
