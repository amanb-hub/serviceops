export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  message: string;
}

export interface Role {
  id: string;
  name: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  is_active: boolean;
  role: Role;
}

export interface Client {
  id: string;
  name: string;
  code: string;
  contact_name: string | null;
  contact_email: string | null;
  contact_phone: string | null;
  status: string;
}

export interface City {
  id: string;
  name: string;
  state: string | null;
  country: string;
  status: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}
