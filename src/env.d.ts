/// <reference path="../.astro/types.d.ts" />

interface D1PreparedStatement {
  bind(...values: any[]): D1PreparedStatement;
  first<T = unknown>(colName?: string): Promise<T | null>;
  run(): Promise<{ success: boolean; error?: string }>;
  all<T = unknown>(): Promise<{ results: T[]; success: boolean }>;
}

interface D1Database {
  prepare(query: string): D1PreparedStatement;
}

interface Env {
  DB: D1Database;
}

declare namespace App {
  interface Locals {
    runtime?: {
      env: Env;
    };
  }
}