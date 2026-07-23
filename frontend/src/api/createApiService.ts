import { httpClient } from './httpClient'
import type { ApiService, RequestOptions } from './types'

function joinPath(basePath: string, path = '') {
  const base = `/${basePath.replace(/^\/+|\/+$/g, '')}`
  const suffix = path.replace(/^\/+/, '')
  return suffix ? `${base}/${suffix}` : base
}

export function createApiService(basePath: string): ApiService {
  return {
    request<TResponse>(
      path = '',
      options?: RequestOptions & { method?: string },
    ) {
      return httpClient.request<TResponse>(joinPath(basePath, path), options)
    },
    get<TResponse>(path = '', options?: RequestOptions) {
      return httpClient.get<TResponse>(joinPath(basePath, path), options)
    },
    post<TResponse, TBody = unknown>(
      path: string,
      body: TBody,
      options?: RequestOptions,
    ) {
      return httpClient.post<TResponse, TBody>(
        joinPath(basePath, path),
        body,
        options,
      )
    },
    put<TResponse, TBody = unknown>(
      path: string,
      body: TBody,
      options?: RequestOptions,
    ) {
      return httpClient.put<TResponse, TBody>(
        joinPath(basePath, path),
        body,
        options,
      )
    },
    patch<TResponse, TBody = unknown>(
      path: string,
      body: TBody,
      options?: RequestOptions,
    ) {
      return httpClient.patch<TResponse, TBody>(
        joinPath(basePath, path),
        body,
        options,
      )
    },
    delete<TResponse>(path = '', options?: RequestOptions) {
      return httpClient.delete<TResponse>(joinPath(basePath, path), options)
    },
  }
}
