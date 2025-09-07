import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-auth',
  imports: [FormsModule, CommonModule],
  templateUrl: './auth.html',
  styleUrl: './auth.scss'
})
export class AuthComponent {
  isLoginMode = true;
  isLoading = false;
  errorMessage = '';

  // Form data
  loginForm = {
    email: '',
    password: ''
  };

  registerForm = {
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  };

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  toggleMode() {
    this.isLoginMode = !this.isLoginMode;
    this.errorMessage = '';
  }

  onLogin() {
    if (!this.loginForm.email || !this.loginForm.password) {
      this.errorMessage = 'Please fill in all fields';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.login(this.loginForm.email, this.loginForm.password).subscribe({
      next: (success) => {
        this.isLoading = false;
        if (success) {
          this.router.navigate(['/dashboard']);
        } else {
          this.errorMessage = 'Invalid credentials';
        }
      },
      error: () => {
        this.isLoading = false;
        this.errorMessage = 'Login failed';
      }
    });
  }

  onRegister() {
    if (!this.registerForm.name || !this.registerForm.email || !this.registerForm.password) {
      this.errorMessage = 'Please fill in all fields';
      return;
    }

    if (this.registerForm.password !== this.registerForm.confirmPassword) {
      this.errorMessage = 'Passwords do not match';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    // Generate a valid username from email (before @) or name
    const generateUsername = (name: string, email: string): string => {
      // First try to use the part before @ in email
      let username = email.split('@')[0];
      
      // Remove any invalid characters and replace with underscores
      username = username.replace(/[^a-zA-Z0-9@._+-]/g, '_');
      
      // Remove consecutive underscores and trim
      username = username.replace(/_+/g, '_').replace(/^_|_$/g, '');
      
      // Ensure it's not empty and has at least 3 characters
      if (username.length < 3) {
        username = 'user_' + username;
      }
      
      // Add timestamp to ensure uniqueness
      username = username + '_' + Date.now().toString().slice(-4);
      
      return username;
    };

    const registerData = {
      username: generateUsername(this.registerForm.name, this.registerForm.email),
      email: this.registerForm.email,
      first_name: this.registerForm.name.split(' ')[0] || this.registerForm.name,
      last_name: this.registerForm.name.split(' ').slice(1).join(' ') || '',
      password: this.registerForm.password,
      password_confirm: this.registerForm.password
    };

    this.authService.register(registerData).subscribe({
      next: (success) => {
        this.isLoading = false;
        if (success) {
          this.router.navigate(['/dashboard']);
        } else {
          this.errorMessage = 'Registration failed';
        }
      },
      error: () => {
        this.isLoading = false;
        this.errorMessage = 'Registration failed';
      }
    });
  }
}
