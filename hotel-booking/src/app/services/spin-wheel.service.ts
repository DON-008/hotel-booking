import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface Prize {
  id: string;
  name: string;
  description: string;
  icon: string;
  probability: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface SpinWheelGame {
  id: string;
  customer: string;
  customer_name: string;
  played_at: string;
  prize_won: string;
  prize_name: string;
  prize_icon: string;
  is_claimed: boolean;
  claimed_at?: string;
  notes?: string;
}

export interface GameSession {
  id: string;
  customer: string;
  customer_name: string;
  has_played: boolean;
  first_play_date?: string;
  created_at: string;
  updated_at: string;
}

export interface SpinWheelPlayRequest {
  customer_id: string;
}

export interface SpinWheelResult {
  prize: Prize;
  customer_name: string;
  played_at: string;
  is_first_play: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class SpinWheelService {
  constructor(private apiService: ApiService) { }

  // Prizes
  getPrizes(): Observable<Prize[]> {
    return this.apiService.get<Prize[]>('/spin-wheel/prizes/');
  }

  getPrize(id: string): Observable<Prize> {
    return this.apiService.get<Prize>(`/spin-wheel/prizes/${id}/`);
  }

  createPrize(prize: Partial<Prize>): Observable<Prize> {
    return this.apiService.post<Prize>('/spin-wheel/prizes/', prize);
  }

  updatePrize(id: string, prize: Partial<Prize>): Observable<Prize> {
    return this.apiService.put<Prize>(`/spin-wheel/prizes/${id}/`, prize);
  }

  deletePrize(id: string): Observable<void> {
    return this.apiService.delete<void>(`/spin-wheel/prizes/${id}/`);
  }

  getActivePrizes(): Observable<Prize[]> {
    return this.apiService.get<Prize[]>('/spin-wheel/prizes/active/');
  }

  // Spin Wheel Games
  getGames(): Observable<SpinWheelGame[]> {
    return this.apiService.get<SpinWheelGame[]>('/spin-wheel/games/');
  }

  getGame(id: string): Observable<SpinWheelGame> {
    return this.apiService.get<SpinWheelGame>(`/spin-wheel/games/${id}/`);
  }

  playSpinWheel(request: SpinWheelPlayRequest): Observable<SpinWheelResult> {
    return this.apiService.post<SpinWheelResult>('/spin-wheel/games/play/', request);
  }

  claimPrize(gameId: string, notes?: string): Observable<SpinWheelGame> {
    return this.apiService.patch<SpinWheelGame>(`/spin-wheel/games/${gameId}/claim/`, {
      notes: notes || ''
    });
  }

  getGamesStats(): Observable<{
    total_games: number;
    claimed_prizes: number;
    unclaimed_prizes: number;
    prize_distribution: { [key: string]: number };
  }> {
    return this.apiService.get<{
      total_games: number;
      claimed_prizes: number;
      unclaimed_prizes: number;
      prize_distribution: { [key: string]: number };
    }>('/spin-wheel/games/stats/');
  }

  // Game Sessions
  getGameSessions(): Observable<GameSession[]> {
    return this.apiService.get<GameSession[]>('/spin-wheel/sessions/');
  }

  getGameSession(id: string): Observable<GameSession> {
    return this.apiService.get<GameSession>(`/spin-wheel/sessions/${id}/`);
  }

  updateGameSession(id: string, session: Partial<GameSession>): Observable<GameSession> {
    return this.apiService.put<GameSession>(`/spin-wheel/sessions/${id}/`, session);
  }

  deleteGameSession(id: string): Observable<void> {
    return this.apiService.delete<void>(`/spin-wheel/sessions/${id}/`);
  }

  getPlayedCustomers(): Observable<GameSession[]> {
    return this.apiService.get<GameSession[]>('/spin-wheel/sessions/played-customers/');
  }

  getAvailableCustomers(): Observable<any[]> {
    return this.apiService.get<any[]>('/spin-wheel/sessions/available-customers/');
  }
}
