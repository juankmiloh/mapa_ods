import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { IEmpresa, ISUIError } from 'src/app/models/IOptionsMapa.model';
import { AppObservableService } from 'src/app/services/app-observable.service';
import { SuiService } from 'src/app/services/sui.service';

@Component({
  selector: 'app-modal-empresa',
  templateUrl: './modal-empresa.component.html',
  styleUrls: ['./modal-empresa.component.scss'],
})
export class ModalEmpresaComponent implements OnInit {

  selectEmpresa: any;
  selectDpto: any = '';
  selectMpio: any = '';
  selectCpoblado: any = '';
  loadEmpresas = false;
  suiEmpresas: any[] = [];
  suiDivipolaDpto: any[] = [];
  suiDivipolaMpio: any[] = [];
  suiDivipolaCpoblado: any = [];
  loadSuiDpto: boolean;
  loadSuiMpio: boolean = true;
  loadSuiCpoblado: boolean = true;
  idDepto: any;
  idMpio: any;
  idCpoblado: any;

  constructor(
    private formBuilder: FormBuilder,
    private suiService: SuiService,
    public observer: AppObservableService,
    private dialogRef: MatDialogRef<ModalEmpresaComponent>,
  ) {
    this.filteredEmpresas = this.optionsMap.get('empresa').valueChanges
      .pipe(
        startWith(''),
        map(state => state ? this._filterStates(state) : this.suiEmpresas.slice()),
      );
      this.filteredDepartamentos = this.optionsMap.get('departamento').valueChanges
        .pipe(
          startWith(''),
          map(state => state ? this._filterStatesDpto(state) : this.suiDivipolaDpto.slice()),
        );
      this.filteredMunicipios = this.optionsMap.get('municipio').valueChanges
        .pipe(
          startWith(''),
          map(state => state ? this._filterStatesMpio(state) : this.suiDivipolaMpio.slice()),
        );
      this.filteredCpoblados = this.optionsMap.get('cpoblado').valueChanges
        .pipe(
          startWith(''),
          map(state => state ? this._filterStatesCpoblado(state) : this.suiDivipolaCpoblado.slice()),
        );
    }

  optionsMap = this.formBuilder.group({
    empresa: [null, Validators.required],
    departamento: [null],
    municipio: [null],
    cpoblado: [null],
  });
  filteredEmpresas: Observable<IEmpresa[]>;
  filteredDepartamentos: Observable<any[]>;
  filteredMunicipios: Observable<any[]>;
  filteredCpoblados: Observable<any[]>;

  ngOnInit(): void {
    this.loadEmpresas = true;
    this.loadSuiDpto = true;
    const servicio = JSON.parse(localStorage.getItem('servicio'));
    this.loadSuiDivipolaDepto({optiondpto: 'depto', optionmpio: 'null', optioncpoblado: 'null', dpto: 0, mpio: 0, cpoblado: 0});
    this.loadSuiEmpresas(servicio);
    this.observer.setChangeDepto({cod: 'TODOS', nombre: 'TODOS'}); // Se reinician para que no queden pegados valores
    this.observer.setChangeMpio({cod: 'TODOS', nombre: 'TODOS'});
    this.observer.setChangeCpoblado({cod: 'TODOS', nombre: 'TODOS'});
  }

  // Se hace llamado al servicio para cargar empresas
  loadSuiEmpresas(servicio) {
    this.suiService.getEmpresasServicio(servicio['cod_servicio']).subscribe(empresas => {
      // console.log(this.suiEmpresas);
      this.suiEmpresas = empresas;
      this.suiEmpresas.unshift({
        id_empresa: 0,
        nombre: 'TODAS',
        sigla: 'TODAS',
        nit: 0,
        cod_servicio: servicio['cod_servicio'],
        servicio: servicio['servicio'],
      });
      this.selectEmpresa = 'TODAS';
      this.loadEmpresas = false;
      // Se cargan los datos si ya habido una empresa seleccionada
      const loadData = JSON.parse(localStorage.getItem('empresa'));
      if (loadData) {
        if (loadData.cod_servicio === servicio.cod_servicio) { // Si la empresa seleccionada es del mismo servicio que esta seleccionado
          this.selectEmpresa = loadData.nombre;
        }
      }
    }, (error: ISUIError) => {
      this.observer.setShowAlertErrorSUI(error.status);
    });
  }

  // Se hace llamado al servicio para cargar DIVIPOLA DEPARTAMENTO
  loadSuiDivipolaDepto(objDivipola) {
    this.suiService.getDivipola(objDivipola).subscribe(resp => {
      console.log('DIVIPOLA DEPTO --> ', resp);
      this.suiDivipolaDpto = resp;
      this.suiDivipolaDpto.unshift({
        cod: 0,
        nombre: 'TODOS',
      });
      this.loadSuiDpto = false;
    }, (error: ISUIError) => {
      this.observer.setShowAlertErrorSUI(error.status);
    });
  }

  // Se hace llamado al servicio para cargar DIVIPOLA MUNICIPIO
  loadSuiDivipolaMpio(objDivipola) {
    this.suiService.getDivipola(objDivipola).subscribe(resp => {
      // console.log('DIVIPOLA MPIO --> ', resp);
      this.suiDivipolaMpio = resp;
      this.suiDivipolaMpio.unshift({
        cod: 0,
        nombre: 'TODOS',
      });
      this.loadSuiMpio = false;
    }, (error: ISUIError) => {
      this.observer.setShowAlertErrorSUI(error.status);
    });
  }

  // Se hace llamado al servicio para cargar DIVIPOLA CENTROSPOBLADOS
  loadSuiDivipolaCpoblado(objDivipola) {
    this.suiService.getDivipola(objDivipola).subscribe(resp => {
      console.log('DIVIPOLA MPIO --> ', resp);
      this.suiDivipolaCpoblado = resp;
      this.loadSuiCpoblado = false;
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

  // permitir filtrar y buscar departamentos
  private _filterStatesDpto(value: string): IEmpresa[] {
    try {
      const filterValue = value.toLowerCase();
      return this.suiDivipolaDpto.filter(state => state.nombre.toLowerCase().indexOf(filterValue) === 0);
    } catch (error) {
      // console.log('filterValue: ', error);
    }
  }

  // permitir filtrar y buscar municipios
  private _filterStatesMpio(value: string): IEmpresa[] {
    try {
      const filterValue = value.toLowerCase();
      return this.suiDivipolaMpio.filter(state => state.nombre.toLowerCase().indexOf(filterValue) === 0);
    } catch (error) {
      // console.log('filterValue: ', error);
    }
  }

  // permitir filtrar y buscar centros poblados
  private _filterStatesCpoblado(value: string): IEmpresa[] {
    try {
      const filterValue = value.toLowerCase();
      return this.suiDivipolaCpoblado.filter(state => state.nombre.toLowerCase().indexOf(filterValue) === 0);
    } catch (error) {
      // console.log('filterValue: ', error);
    }
  }

  setOptionDpto(paramDpto) {
    console.log('OPTION SELECTED DPTO --> ', paramDpto);
    this.selectMpio = '';
    this.selectCpoblado = '';
    this.suiDivipolaCpoblado = [];
    this.idDepto = this.suiDivipolaDpto.find(depto => paramDpto === depto.nombre).cod;
    if (this.idDepto === 0 && paramDpto === 'TODOS') {
      this.observer.setChangeDepto({cod: 'TODOS', nombre: paramDpto});
    } else {
      this.observer.setChangeDepto({cod: this.idDepto, nombre: paramDpto});
    }
    this.loadSuiMpio = true;
    this.loadSuiDivipolaMpio({optiondpto: 'null', optionmpio: 'mpio', optioncpoblado: 'null', dpto: this.idDepto, mpio: 0, cpoblado: 0});
  }

  setOptionMpio(paramMpio) {
    console.log('OPTION SELECTED MPIO --> ', paramMpio);
    this.selectCpoblado = '';
    this.suiDivipolaCpoblado = [];
    this.idMpio = this.suiDivipolaMpio.find(mpio => paramMpio === mpio.nombre).cod;
    if (this.idMpio === 0 && paramMpio === 'TODOS') {
      this.observer.setChangeMpio({cod: 'TODOS', nombre: paramMpio});
    } else {
      this.observer.setChangeMpio({cod: this.idMpio, nombre: paramMpio});
    }
    if (paramMpio !== 'TODOS') {
      this.loadSuiCpoblado = true;
      // tslint:disable-next-line: max-line-length
      this.loadSuiDivipolaCpoblado({optiondpto: 'null', optionmpio: 'null', optioncpoblado: 'cpoblado', dpto: this.idDepto, mpio: this.idMpio, cpoblado: 0});
    }
  }

  setOptionCpoblado(paramCpoblado) {
    console.log('OPTION SELECTED CPOBLADO --> ', paramCpoblado);
    this.idCpoblado = this.suiDivipolaCpoblado.find(cPoblado => paramCpoblado === cPoblado.nombre).cod;
    if (this.idCpoblado === 0 && paramCpoblado === 'TODOS') {
      this.observer.setChangeCpoblado({cod: 'TODOS', nombre: paramCpoblado});
    } else {
      this.observer.setChangeCpoblado({cod: this.idCpoblado, nombre: paramCpoblado});
    }
  }

  // enviar valores al padre
  sendDataParent() {
    const idEmpresa = this.suiEmpresas.find(empresa => this.selectEmpresa === empresa.nombre).id_empresa;
    const codServicio = this.suiEmpresas.find(empresa => this.selectEmpresa === empresa.nombre).cod_servicio;
    const nombreServicio = this.suiEmpresas.find(empresa => this.selectEmpresa === empresa.nombre).servicio;
    // tslint:disable-next-line: max-line-length
    const model = {id_empresa: idEmpresa, nombre: this.selectEmpresa, cod_servicio: codServicio, servicio: nombreServicio };
    const data = { modal: 'empresa', value: model };
    this.dialogRef.close(data);
  }
}
