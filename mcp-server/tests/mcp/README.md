# MCP Testing Suite - Essential Tests

This directory contains the **4 most essential MCP tests** for the SSMS MCP Server, providing comprehensive coverage without redundancy.

## 📁 Essential Test Files

### **Core Tests**
- **`verify_mcp_server.py`** - **MOST IMPORTANT** - Verifies MCP server initialization and all components
- **`test_database_connections.py`** - **CRITICAL** - Tests database connections and basic operations
- **`test_mcp_tools.py`** - **IMPORTANT** - Tests individual MCP tools functionality
- **`test_mcp_resources.py`** - **IMPORTANT** - Tests individual MCP resources functionality

### **Test Runner**
- **`run_all_tests.py`** - Runs all 4 essential tests in sequence with summary
- **`ESSENTIAL_TESTS.md`** - Detailed explanation of the simplified test suite

## 🚀 **Quick Start**

### **Run All Tests**
```bash
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
python tests/mcp/run_all_tests.py
```

### **Run Individual Tests**
```bash
# Test database connections
python tests/mcp/test_database_connections.py

# Verify MCP server
python tests/mcp/verify_mcp_server.py

# Test MCP tools
python tests/mcp/test_mcp_tools.py

# Test MCP resources
python tests/mcp/test_mcp_resources.py
```

## 📊 **Test Coverage**

### **Database Tests**
- ✅ Master database connection (KonaAI)
- ✅ Data Management database connection (DIT_GDB)
- ✅ Table enumeration
- ✅ Basic query execution
- ✅ Connection pooling

### **MCP Server Tests**
- ✅ Server initialization
- ✅ Component registration
- ✅ Database connections
- ✅ Tool registration (11 tools)
- ✅ Resource registration (4 resources)

### **MCP Tools Tests**
- ✅ Query tool execution
- ✅ Schema tool functionality
- ✅ CRUD tool operations
- ✅ Error handling

### **MCP Resources Tests**
- ✅ Tables resource listing
- ✅ Procedures resource listing
- ✅ Triggers resource listing
- ✅ Views resource listing

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Ensure you're in the mcp-server directory
cd "C:\Users\UdayChaitanyaGurvind\Desktop\KonaAi\KonaAI Web Application\KonaAI-SSMS-MCP\mcp-server"
```

#### **Database Connection Errors**
- Check SQL Server is running
- Verify Windows Authentication is enabled
- Ensure database access permissions

#### **MCP Server Errors**
- Check all dependencies are installed
- Verify configuration is correct
- Test individual components

### **Debug Steps**

1. **Run database connection test first**
2. **Verify MCP server initialization**
3. **Test individual tools and resources**
4. **Check for any error messages**

## 📋 **Expected Results**

### **Successful Test Output**
```
Database Connections Testing
==============================
OK Configuration loaded

Testing Master Database:
OK Master database connected
   Tables found: 29
   Testing query on App.Client
   Query successful: 1 rows returned

Testing Data Management Database:
OK Data Management database connected
   Tables found: 367
   Testing query on Analytics.CustomerMaster
   Query successful: 1 rows returned

Database connections testing completed!
```

### **MCP Server Verification**
```
MCP Server Verification
==============================
OK Server initialized successfully

Checking MCP Server Components:
OK Master database connection configured
OK Data Management database connection configured
OK Query tool registered
OK CRUD tool registered
OK Schema tool registered
OK Stored procedure tool registered
OK Tables resource registered
OK Procedures resource registered
OK Triggers resource registered
OK Views resource registered

Testing Database Connections:
OK Master database: 29 tables found
OK Data Management database: 367 tables found

MCP Server verification completed!
```

## 🎯 **Usage Guidelines**

### **Before Development**
- Run `verify_mcp_server.py` to ensure server is working
- Run `test_database_connections.py` to verify database access

### **After Changes**
- Run `run_all_tests.py` to verify all functionality
- Test specific components if issues arise

### **For Debugging**
- Run individual tests to isolate issues
- Check error messages for specific problems
- Verify database connections first

## 📞 **Support**

If tests fail:
1. Check the error messages
2. Verify database connections
3. Ensure all dependencies are installed
4. Test individual components
5. Check configuration settings

---

**This testing suite ensures your MCP server is working correctly! 🚀**


