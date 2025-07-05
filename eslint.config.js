// eslint.config.js
import vue from 'eslint-plugin-vue';
import js from '@eslint/js';
import ts from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import prettier from 'eslint-plugin-prettier';
import vueParser from 'vue-eslint-parser';
import { defineConfig } from 'eslint/config';
import globals from 'globals';

export default defineConfig([
  {
    ignores: ['src-tauri/**', '*.d.ts']
  },
  js.configs.recommended,
  ...vue.configs['flat/essential'],
  ...ts.configs['flat/recommended'],
  {
    files: ['**/*.ts', '**/*.vue'],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tsParser,
        ecmaVersion: 'latest',
        sourceType: 'module',
        extraFileExtensions: ['.vue']
      },
      globals: {
        ...globals.browser
      }
    }
  },
  {
    plugins: {
      vue,
      '@typescript-eslint': ts,
      prettier
    },
    rules: {
      'prettier/prettier': 'warn',
      'vue/multi-word-component-names': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      'no-constant-binary-expression': 'off',
      '@typescript-eslint/no-empty-object-type': 'off'
    }
  }
]);
