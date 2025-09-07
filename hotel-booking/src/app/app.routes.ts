import { Routes } from '@angular/router';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
  // Default redirect to dashboard
  { 
    path: '', 
    redirectTo: '/dashboard', 
    pathMatch: 'full' 
  },
  
  // Authentication route (not protected)
  { 
    path: 'auth', 
    loadComponent: () => import('./components/auth/auth').then(m => m.AuthComponent)
  },
  
  // Protected routes with lazy loading
  { 
    path: 'dashboard', 
    loadComponent: () => import('./components/dashboard/dashboard').then(m => m.DashboardComponent),
    canActivate: [authGuard]
  },
  { 
    path: 'events', 
    loadComponent: () => import('./components/events/events').then(m => m.EventsComponent),
    canActivate: [authGuard]
  },
  { 
    path: 'offers', 
    loadComponent: () => import('./components/offers/offers').then(m => m.OffersComponent),
    canActivate: [authGuard]
  },
  { path: 'spin-wheel', loadComponent: () => import('./components/spin-wheel/spin-wheel').then(m => m.SpinWheelComponent) },
  
  // Wildcard route - redirect to dashboard
  { 
    path: '**', 
    redirectTo: '/dashboard' 
  }
];
