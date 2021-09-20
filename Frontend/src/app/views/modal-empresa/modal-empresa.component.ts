import { Component, OnInit } from '@angular/core';
import { FormControl, FormBuilder, Validators } from '@angular/forms';
import * as moment from 'moment';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { IEmpresa, ISUIError } from 'src/app/models/IOptionsMapa.model';
import { AppObservableService } from 'src/app/services/app-observable.service';
import { SuiService } from 'src/app/services/sui.service';

@Component({
  selector: 'app-modal-empresa',
  templateUrl: './modal-empresa.component.html',
  styleUrls: ['./modal-empresa.component.scss']
})
export class ModalEmpresaComponent implements OnInit {

  selectEmpresa: string;
  public suiEmpresas: any[] = [];
  loadEmpresas = false;

  constructor(
    private formBuilder: FormBuilder,
    private suiService: SuiService,
    public observer: AppObservableService
  ) {
    this.filteredEmpresas = this.optionsMap.get('empresa').valueChanges
      .pipe(
        startWith(''),
        map(state => state ? this._filterStates(state) : this.suiEmpresas.slice()),
      );
  }
  
  optionsMap = this.formBuilder.group({
    empresa: [null, Validators.required]
  });
  filteredEmpresas: Observable<IEmpresa[]>;
  
  ngOnInit(): void {
    this.loadEmpresas = true;
    this.loadSuiEmpresas();
  }

  // Se hace llamado al servicio para cargar empresas
  loadSuiEmpresas() {
    this.suiService.getEmpresas().subscribe( empresas => {
      this.suiEmpresas = empresas;
      this.suiEmpresas.unshift({
        cod_empresa: 0,
        nombre: 'TODAS',
        servicio: 'ENERGIA',
      });
      this.selectEmpresa = 'TODAS';
      this.loadEmpresas = false;
    }, (error: ISUIError) => {
      this.observer.setShowAlertErrorSUI(error.status);
    });
  }

  // permitir filtrar y buscar empresas
  private _filterStates(value: string): IEmpresa[] {
    try {
      const filterValue = value.toLowerCase();
      return this.suiEmpresas.filter(state => state.nombre.toLowerCase().indexOf(filterValue) === 0);
    } catch (error) {
      // console.log('filterValue: ', error);
    }
  }

  // enviar valores al padre
  sendDataParent() {
    console.log('object');
  }

  // se ejecuta cuando se cambien valores del año
  somethingChanged(select: any): void {
    // const mesActual = this.optionsMap.get('mes').value.format('M') - 1;
    // this.startDate = new Date(select, mesActual, 1); // Actualizar año y mes seleccionado en el modal de meses
  }

}
