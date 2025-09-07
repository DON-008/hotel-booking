import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { OffersService, Offer, OfferCreate, PaginatedResponse } from '../../services/offers.service';

@Component({
  selector: 'app-offers',
  imports: [CommonModule, FormsModule],
  templateUrl: './offers.html',
  styleUrl: './offers.scss'
})
export class OffersComponent implements OnInit {
  showOfferForm = false;
  isEditMode = false;
  loading = false;
  error: string | null = null;
  
  offerTypes = ['percentage', 'fixed'];
  
  newOffer = {
    title: '',
    description: '',
    discount: 0,
    type: 'percentage',
    validFrom: '',
    validTo: '',
    status: 'active'
  };

  offers: any[] = []; // Will be populated by API with proper typing

  constructor(
    private router: Router,
    private offersService: OffersService
  ) {}

  ngOnInit() {
    this.loadOffers();
  }

  loadOffers() {
    this.loading = true;
    this.error = null;
    console.log('Loading offers from API...');
    
    this.offersService.getOffers().subscribe({
      next: (response: PaginatedResponse<Offer>) => {
        console.log('Offers API response:', response);
        
        // Handle paginated response - extract results array
        const data = response.results;
        console.log('Extracted offers data array:', data);
        
        // Map API data to template-compatible format
        this.offers = data.map((offer: Offer) => ({
          id: offer.id, // Keep as string since it's a UUID
          title: offer.title,
          description: offer.description,
          discount: typeof offer.discount_value === 'string' ? parseFloat(offer.discount_value) : offer.discount_value, // Convert to number
          type: offer.offer_type,
          validFrom: offer.valid_from,
          validTo: offer.valid_to,
          status: offer.status
        }));
        this.loading = false;
        console.log('Mapped offers:', this.offers);
      },
      error: (error) => {
        this.error = 'Failed to load offers';
        this.loading = false;
        console.error('Error loading offers:', error);
        console.error('Error details:', error.error);
        console.error('Error status:', error.status);
      }
    });
  }

  get activeOffersCount(): number {
    return this.offers.filter(o => o.status === 'active').length;
  }

  get averageDiscount(): number {
    if (this.offers.length === 0) return 0;
    
    // Filter out offers with invalid discount values and calculate average
    const validOffers = this.offers.filter(o => o.discount != null && !isNaN(o.discount));
    if (validOffers.length === 0) return 0;
    
    const total = validOffers.reduce((sum, o) => sum + o.discount, 0);
    const average = total / validOffers.length;
    
    console.log('Average discount calculation:', {
      totalOffers: this.offers.length,
      validOffers: validOffers.length,
      total: total,
      average: average
    });
    
    return Math.round(average * 100) / 100; // Round to 2 decimal places
  }

  getInactiveOffersCount(): number {
    return this.offers.filter(o => o.status !== 'active').length;
  }

  goBack() {
    this.router.navigate(['/dashboard']);
  }

  editOffer(offer: any) {
    console.log('Edit offer:', offer);
    
    // Set the form data for editing
    this.newOffer = {
      title: offer.title,
      description: offer.description,
      discount: offer.discount,
      type: offer.type,
      validFrom: offer.validFrom,
      validTo: offer.validTo,
      status: offer.status
    };
    
    // Set the offer ID for updates
    (this.newOffer as any).id = offer.id;
    
    // Set edit mode and show form
    this.isEditMode = true;
    this.showOfferForm = true;
  }

  deleteOffer(offerId: string) {
    if (confirm('Are you sure you want to delete this offer?')) {
      this.loading = true;
      this.error = null;
      
      this.offersService.deleteOffer(offerId).subscribe({
        next: () => {
          this.loadOffers(); // Reload data
          this.loading = false;
        },
        error: (error) => {
          this.error = 'Failed to delete offer';
          this.loading = false;
          console.error('Error deleting offer:', error);
        }
      });
    }
  }

  toggleStatus(offer: any) {
    const newStatus = offer.status === 'active' ? 'inactive' : 'active';
    console.log(`Toggling offer ${offer.id} status from ${offer.status} to ${newStatus}`);
    
    this.loading = true;
    this.error = null;
    
    const updateData: Partial<OfferCreate> = {
      title: offer.title,
      description: offer.description,
      offer_type: offer.type,
      discount_value: offer.discount,
      valid_from: offer.validFrom,
      valid_to: offer.validTo,
      status: newStatus
    };
    
    this.offersService.updateOffer(offer.id, updateData).subscribe({
      next: () => {
        console.log(`Successfully updated offer ${offer.id} status to ${newStatus}`);
        this.loadOffers(); // Reload data to reflect changes
        this.loading = false;
      },
      error: (error) => {
        this.error = `Failed to ${newStatus === 'active' ? 'activate' : 'deactivate'} offer`;
        this.loading = false;
        console.error(`Error toggling offer status:`, error);
        console.error('Error details:', error.error);
      }
    });
  }

  // Modal methods
  toggleOfferForm() {
    this.showOfferForm = !this.showOfferForm;
    if (!this.showOfferForm) {
      this.resetForm();
    }
  }

  resetForm() {
    this.newOffer = {
      title: '',
      description: '',
      discount: 0,
      type: 'percentage',
      validFrom: '',
      validTo: '',
      status: 'active'
    };
    this.isEditMode = false;
  }

  saveOffer() {
    if (this.isValidForm()) {
      this.loading = true;
      this.error = null;

      const offerData: OfferCreate = {
        title: this.newOffer.title,
        description: this.newOffer.description,
        offer_type: this.newOffer.type as 'percentage' | 'fixed',
        discount_value: this.newOffer.discount,
        valid_from: this.newOffer.validFrom,
        valid_to: this.newOffer.validTo,
        status: this.newOffer.status as 'active' | 'inactive' | 'expired'
      };

      if (this.isEditMode && (this.newOffer as any).id) {
        // Update existing
        console.log('Updating offer with data:', offerData);
        console.log('Offer ID:', (this.newOffer as any).id);
        
        this.offersService.updateOffer((this.newOffer as any).id, offerData).subscribe({
          next: () => {
            this.loadOffers(); // Reload data
            this.toggleOfferForm();
            this.loading = false;
          },
          error: (error) => {
            this.error = 'Failed to update offer';
            this.loading = false;
            console.error('Error updating offer:', error);
          }
        });
      } else {
        // Add new
        this.offersService.createOffer(offerData).subscribe({
          next: () => {
            this.loadOffers(); // Reload data
            this.toggleOfferForm();
            this.loading = false;
          },
          error: (error) => {
            this.error = 'Failed to create offer';
            this.loading = false;
            console.error('Error creating offer:', error);
          }
        });
      }
    }
  }

  startEditOffer(offer: any) {
    console.log('Starting edit for offer:', offer);
    
    // Set the form data for editing
    this.newOffer = {
      title: offer.title,
      description: offer.description,
      discount: offer.discount,
      type: offer.type,
      validFrom: offer.validFrom,
      validTo: offer.validTo,
      status: offer.status
    };
    
    // Set the offer ID for updates
    (this.newOffer as any).id = offer.id;
    
    // Set edit mode and show form
    this.isEditMode = true;
    this.showOfferForm = true;
  }

  isValidForm(): boolean {
    return !!(this.newOffer.title && 
              this.newOffer.description && 
              this.newOffer.discount > 0 && 
              this.newOffer.validFrom && 
              this.newOffer.validTo);
  }
}
