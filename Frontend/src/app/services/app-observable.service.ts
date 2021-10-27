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
  private changeDepto = new Subject<any>();
  private changeMpio = new Subject<any>();
  private changeCpoblado = new Subject<any>();

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

  setChangeDepto(status: any) {
    this.changeDepto.next(status);
  }

  getChangeDepto(): Observable<any>  {
    return this.changeDepto.asObservable();
  }

  setChangeMpio(status: any) {
    this.changeMpio.next(status);
  }

  getChangeMpio(): Observable<any>  {
    return this.changeMpio.asObservable();
  }

  setChangeCpoblado(status: any) {
    this.changeCpoblado.next(status);
  }

  getChangeCpoblado(): Observable<any>  {
    return this.changeCpoblado.asObservable();
  }
}
