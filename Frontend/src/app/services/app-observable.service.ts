import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AppObservableService {

  private showAlertErrorSUI = new Subject<any>();
  private changeBasemap = new Subject<any>();
  private changePeriodo = new Subject<any>();
  private changeEmpresa = new Subject<any>();
  private changeSector = new Subject<any>();
  private changeServicio = new Subject<any>();

  constructor() {}

  setShowAlertErrorSUI(status: number) {
    this.showAlertErrorSUI.next(status);
  }

  getShowAlertErrorSUI(): Observable<any>  {
    return this.showAlertErrorSUI.asObservable();
  }

  setChangeBasemap(status: string) {
    this.changeBasemap.next(status);
  }

  getChangeBasemap(): Observable<any>  {
    return this.changeBasemap.asObservable();
  }

  setChangePeriodo(status: string) {
    this.changePeriodo.next(status);
  }

  getChangePeriodo(): Observable<any>  {
    return this.changePeriodo.asObservable();
  }

  setChangeEmpresa(status: string) {
    this.changeEmpresa.next(status);
  }

  getChangeEmpresa(): Observable<any>  {
    return this.changeEmpresa.asObservable();
  }

  setChangeSector(status: any) {
    this.changeSector.next(status);
  }

  getChangeSector(): Observable<any>  {
    return this.changeSector.asObservable();
  }

  setChangeServicio(status: any) {
    this.changeServicio.next(status);
  }

  getChangeServicio(): Observable<any>  {
    return this.changeServicio.asObservable();
  }
}
