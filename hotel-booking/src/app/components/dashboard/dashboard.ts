import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService, User } from '../../services/auth';
import { EventsService } from '../../services/events.service';
import { OffersService } from '../../services/offers.service';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class DashboardComponent implements OnInit {
  currentUser: User | null = null;
  activeEventsCount: number = 0;
  activeOffersCount: number = 0;
  loading: boolean = true;

  constructor(
    private authService: AuthService,
    private router: Router,
    private eventsService: EventsService,
    private offersService: OffersService
  ) {}

  ngOnInit() {
    this.currentUser = this.authService.getCurrentUser();
    this.loadDashboardData();
  }

  loadDashboardData() {
    this.loading = true;
    
    // Load active events count
    this.eventsService.getSpecialDates().subscribe({
      next: (response) => {
        // Count upcoming special dates (next 30 days)
        const today = new Date();
        const nextMonth = new Date(today.getTime() + (30 * 24 * 60 * 60 * 1000));
        
        this.activeEventsCount = response.results.filter((event: any) => {
          const eventDate = new Date(event.special_date);
          return eventDate >= today && eventDate <= nextMonth;
        }).length;
      },
      error: (error) => {
        console.error('Error loading events:', error);
        this.activeEventsCount = 0;
      }
    });

    // Load active offers count
    this.offersService.getOffers().subscribe({
      next: (response) => {
        this.activeOffersCount = response.results.filter((offer: any) => 
          offer.status === 'active'
        ).length;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading offers:', error);
        this.activeOffersCount = 0;
        this.loading = false;
      }
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/auth']);
  }

  navigateTo(route: string) {
    this.router.navigate([route]);
  }
}
