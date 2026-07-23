export class ApiError extends Error {
  constructor(message: string, options?: ErrorOptions) {
    super(message, options)
    this.name = 'ApiError'
  }
}

export class HttpError<T = unknown> extends ApiError {
  readonly status: number
  readonly statusText: string
  readonly data: T

  constructor(
    message: string,
    status: number,
    statusText: string,
    data: T,
  ) {
    super(message)
    this.name = 'HttpError'
    this.status = status
    this.statusText = statusText
    this.data = data
  }
}

export class NetworkError extends ApiError {
  constructor(message = 'No fue posible conectar con el servidor.', cause?: unknown) {
    super(message, { cause })
    this.name = 'NetworkError'
  }
}

export function isHttpError(error: unknown): error is HttpError {
  return error instanceof HttpError
}

export function isNetworkError(error: unknown): error is NetworkError {
  return error instanceof NetworkError
}
