import api from "./api";

export interface LoginCredentials {
  username: string;
  password: string;
}

export type SignupCredentials = LoginCredentials;

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const formData = new FormData();
    formData.append("username", credentials.username);
    formData.append("password", credentials.password);

    const response = await api.post<TokenResponse>("/auth/login", formData);
    if (response.data.access_token) {
      localStorage.setItem("token", response.data.access_token);
    }
    return response.data;
  }

  async signup(credentials: SignupCredentials): Promise<void> {
    await api.post("/auth/signup", credentials);
  }

  logout(): void {
    localStorage.removeItem("token");
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem("token");
  }
}

export const authService = new AuthService();
