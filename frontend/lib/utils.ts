import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export interface Server {
  id: string
  name: string
  loader: string
  game_version: string
}

export interface ServerCreate {
  name: string
  loader: string
  game_version: string
}
