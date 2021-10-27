import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap} from 'rxjs/operators';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root',
})
export class SuiService {

  constructor(public http: HttpClient) { }

  serverUrl = environment.serverUrl;

  verifyConnectionSUI() {
    return new Promise((resolve, reject) => {
      this.http.get<any[]>(`${this.serverUrl}/anios`).toPromise().then(res => {
        resolve(res);
      }, (error) => {
        resolve(error);
      });
    });
  }

  getAnios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.serverUrl}/anios`).pipe(
      tap((data) => {
        // console.log(data);
      }), catchError(this.handleError),
      );
  }

  getEmpresasServicio(servicio: number) {
    return this.http.get<any[]>(`${this.serverUrl}/empresas?servicio=${servicio}`).pipe(
      tap((data) => {
        // console.log('Carga empresas exitosa!');
      }), catchError(this.handleError),
    );
  }

  getDivipola(param: any) {
    return this.http.get<any[]>(`${this.serverUrl}/divipola?optiondpto=${param.optiondpto}&optionmpio=${param.optionmpio}&optioncpoblado=${param.optioncpoblado}&dpto=${param.dpto}&mpio=${param.mpio}&cpoblado=${param.cpoblado}`).pipe(
      tap((data) => {
        // console.log('Carga empresas exitosa!');
      }), catchError(this.handleError),
    );
  }

  // Capturamos el estado del error y el mensaje
  private handleError(err: HttpErrorResponse) {
    const error = {
      status: err.status,
      message: err.message,
    };
    return throwError(error);
  }

}
