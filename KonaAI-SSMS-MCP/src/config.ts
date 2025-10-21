import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

export interface DatabaseConfig {
  server: string;
  database: string;
  options: {
    encrypt: boolean;
    trustServerCertificate: boolean;
    enableArithAbort: boolean;
    requestTimeout: number;
    connectionTimeout: number;
  };
}

export interface AppConfig {
  masterDb: DatabaseConfig;
  dataMgmtDb: DatabaseConfig;
  queryTimeout: number;
  maxRows: number;
  logLevel: string;
}

const createDatabaseConfig = (server: string, database: string): DatabaseConfig => ({
  server,
  database,
  options: {
    encrypt: true,
    trustServerCertificate: true,
    enableArithAbort: true,
    requestTimeout: parseInt(process.env.QUERY_TIMEOUT || '30000'),
    connectionTimeout: 15000
  }
});

export const config: AppConfig = {
  masterDb: createDatabaseConfig(
    process.env.MASTER_DB_SERVER || 'dc-l-',
    process.env.MASTER_DB_NAME || 'KonaAI'
  ),
  dataMgmtDb: createDatabaseConfig(
    process.env.DATA_MGMT_DB_SERVER || 'dc-l-',
    process.env.DATA_MGMT_DB_NAME || 'DIT_GDB'
  ),
  queryTimeout: parseInt(process.env.QUERY_TIMEOUT || '30000'),
  maxRows: parseInt(process.env.MAX_ROWS || '1000'),
  logLevel: process.env.LOG_LEVEL || 'info'
};

export const getConnectionString = (dbConfig: DatabaseConfig): string => {
  return `Server=${dbConfig.server};Database=${dbConfig.database};Trusted_Connection=true;Encrypt=true;TrustServerCertificate=true;`;
};

export const getDatabaseName = (type: 'master' | 'datamgmt'): string => {
  return type === 'master' ? config.masterDb.database : config.dataMgmtDb.database;
};
