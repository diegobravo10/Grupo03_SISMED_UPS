import { API_URL } from './config'
import { HttpError, NetworkError } from './errors'
import type { QueryParams, RequestOptions } from './types'

function createQueryString(query?: QueryParams) {
  if (!query) return ''

  const params = new URLSearchParams()

  Object.entries(query).forEach(([key, value]) => {
    const values = Array.isArray(value) ? value : [value]
    values.forEach((item) => {
      if (item !== null && item !== undefined) {
        params.append(key, String(item))
      }
    })
  })

  const queryString = params.toString()
  return queryString ? `?${queryString}` : ''
}

function buildUrl(path: string, query?: QueryParams) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${API_URL}${normalizedPath}${createQueryString(query)}`
}

function getErrorMessage(data: unknown, response: Response) {
  if (typeof data === 'object' && data !== null && 'detail' in data) {
    const detail = data.detail
    if (typeof detail === 'string') return detail
  }

  if (typeof data === 'string' && data.trim()) return data
  return `La solicitud falló con el estado ${response.status}.`
}

async function parseResponse(response: Response): Promise<unknown> {
  if (response.status === 204) return undefined

  const contentType = response.headers.get('content-type') ?? ''
  if (contentType.includes('application/json')) {
    return response.json()
  }

  const text = await response.text()
  return text || undefined
}

async function request<TResponse>(
  path: string,
  options: RequestOptions & { method?: string } = {},
): Promise<TResponse> {
  const { body, headers, query, ...requestInit } = options
  const isFormData = body instanceof FormData
  const requestHeaders = new Headers(headers)

  if (body !== undefined && !isFormData && !requestHeaders.has('Content-Type')) {
    requestHeaders.set('Content-Type', 'application/json')
  }

  try {
    const response = await fetch(buildUrl(path, query), {
      ...requestInit,
      headers: requestHeaders,
      body:
        body === undefined
          ? undefined
          : isFormData
            ? body
            : JSON.stringify(body),
    })
    const data = await parseResponse(response)

    if (!response.ok) {
      throw new HttpError(
        getErrorMessage(data, response),
        response.status,
        response.statusText,
        data,
      )
    }

    return data as TResponse
  } catch (error) {
    if (error instanceof HttpError) throw error
    if (error instanceof DOMException && error.name === 'AbortError') throw error

    throw new NetworkError(
      'No fue posible conectar con la API de SISMED.',
      error,
    )
  }
}

export const httpClient = {
  baseUrl: API_URL,
  request,
  get<TResponse>(path: string, options?: RequestOptions) {
    return request<TResponse>(path, { ...options, method: 'GET' })
  },
  post<TResponse, TBody = unknown>(
    path: string,
    body: TBody,
    options?: RequestOptions,
  ) {
    return request<TResponse>(path, { ...options, method: 'POST', body })
  },
  put<TResponse, TBody = unknown>(
    path: string,
    body: TBody,
    options?: RequestOptions,
  ) {
    return request<TResponse>(path, { ...options, method: 'PUT', body })
  },
  patch<TResponse, TBody = unknown>(
    path: string,
    body: TBody,
    options?: RequestOptions,
  ) {
    return request<TResponse>(path, { ...options, method: 'PATCH', body })
  },
  delete<TResponse>(path: string, options?: RequestOptions) {
    return request<TResponse>(path, { ...options, method: 'DELETE' })
  },
}
