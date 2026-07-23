export type QueryValue = string | number | boolean | null | undefined
export type QueryParams = Record<string, QueryValue | QueryValue[]>

export interface RequestOptions
  extends Omit<RequestInit, 'body' | 'method'> {
  body?: unknown
  query?: QueryParams
}

export interface ApiService {
  request<TResponse>(
    path?: string,
    options?: RequestOptions & { method?: string },
  ): Promise<TResponse>
  get<TResponse>(path?: string, options?: RequestOptions): Promise<TResponse>
  post<TResponse, TBody = unknown>(
    path: string,
    body: TBody,
    options?: RequestOptions,
  ): Promise<TResponse>
  put<TResponse, TBody = unknown>(
    path: string,
    body: TBody,
    options?: RequestOptions,
  ): Promise<TResponse>
  patch<TResponse, TBody = unknown>(
    path: string,
    body: TBody,
    options?: RequestOptions,
  ): Promise<TResponse>
  delete<TResponse>(
    path?: string,
    options?: RequestOptions,
  ): Promise<TResponse>
}
