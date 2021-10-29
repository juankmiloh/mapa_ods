import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { IEmpresa, IOptionsEmrepsa, ISUIError, modelEmpresa } from 'src/app/models/IOptionsMapa.model';
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
  model: IOptionsEmrepsa = modelEmpresa;

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
    // console.log('Entro a empresas');
    this.loadEmpresas = true;
    this.loadSuiDpto = true;
    const servicio = JSON.parse(localStorage.getItem('servicio'));
    // const servicio = 	{'cod_servicio': 4, 'servicio': 'Energía'};
    this.loadSuiDivipolaDepto({optiondpto: 'depto', optionmpio: 'null', optioncpoblado: 'null', dpto: 0, mpio: 0, cpoblado: 0});
    this.loadSuiEmpresas(servicio);
  }

  ngOnDestroy() {
    this.model = {empresa: {cod_empresa: null, nombre: null, cod_servicio: null, servicio: null},
    depto: {cod: 'TODOS', nombre: 'TODOS'},
    mpio: {cod: 'TODOS', nombre: 'TODOS'},
    cpoblado: {cod: 'TODOS', nombre: 'TODOS'}};
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
        // tslint:disable-next-line: max-line-length
        if (loadData.empresa.cod_servicio === servicio.cod_servicio) { // Si la empresa seleccionada es del mismo servicio que esta seleccionado
          this.selectEmpresa = loadData.empresa.nombre;
        }
      }
    }, (error: ISUIError) => {
      this.observer.setShowAlertErrorSUI(error.status);
    });
  }

  // Se hace llamado al servicio para cargar DIVIPOLA DEPARTAMENTO
  loadSuiDivipolaDepto(objDivipola) {
    this.suiService.getDivipola(objDivipola).subscribe(resp => {
      // console.log('DIVIPOLA DEPTO --> ', resp);
      this.suiDivipolaDpto = resp;
      this.suiDivipolaDpto.unshift({
        cod: 0,
        nombre: 'TODOS',
      });
      this.loadSuiDpto = false;
      this.selectDpto = '';
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
      // console.log('DIVIPOLA MPIO --> ', resp);
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

  changeOptionDpto(evt) {
    // console.log('Escribiendo en el input depto!');
    this.selectMpio = '';
    this.selectCpoblado = '';
    this.suiDivipolaMpio = [];
    this.suiDivipolaCpoblado = [];
  }

  changeOptionMpio(evt) {
    // console.log('Escribiendo en el input mpio!');
    this.selectCpoblado = '';
    this.suiDivipolaCpoblado = [];
  }

  setOptionDpto(paramDpto) {
    // console.log('OPTION SELECTED DPTO --> ', paramDpto);
    this.selectMpio = '';
    this.selectCpoblado = '';
    this.suiDivipolaMpio = [];
    this.suiDivipolaCpoblado = [];
    const idDepto = this.suiDivipolaDpto.find(depto => paramDpto === depto.nombre).cod;
    if (idDepto === 0 && paramDpto === 'TODOS') {
      this.model['depto'] = {cod: 'TODOS', nombre: paramDpto};
    } else {
      this.model['depto'] = {cod: idDepto, nombre: paramDpto};
    }
    this.loadSuiMpio = true;
    this.loadSuiDivipolaMpio({optiondpto: 'null', optionmpio: 'mpio', optioncpoblado: 'null', dpto: idDepto, mpio: 0, cpoblado: 0});
  }

  setOptionMpio(paramMpio) {
    // console.log('OPTION SELECTED MPIO --> ', paramMpio);
    this.selectCpoblado = '';
    this.suiDivipolaCpoblado = [];
    const idMpio = this.suiDivipolaMpio.find(mpio => paramMpio === mpio.nombre).cod; // Obtenemos el id del municipio
    const depto = this.suiDivipolaMpio.find(mpio => paramMpio === mpio.nombre).cod_depto; // Obtenemos el id del departamento

    // console.log('Departamento partiendo de municipio --> ', depto);
    if (idMpio === 0 && paramMpio === 'TODOS') {
      this.model['mpio'] = {cod: 'TODOS', nombre: paramMpio};
    } else {
      this.model['mpio'] = {cod: idMpio, nombre: paramMpio};
    }
    if (paramMpio !== 'TODOS') {
      this.loadSuiCpoblado = true;
      // tslint:disable-next-line: max-line-length
      this.loadSuiDivipolaCpoblado({optiondpto: 'null', optionmpio: 'null', optioncpoblado: 'cpoblado', dpto: depto, mpio: idMpio, cpoblado: 0});
    }
  }

  setOptionCpoblado(paramCpoblado) {
    // console.log('OPTION SELECTED CPOBLADO --> ', paramCpoblado);
    const idCpoblado = this.suiDivipolaCpoblado.find(cPoblado => paramCpoblado === cPoblado.nombre).cod;
    if (idCpoblado === 0 && paramCpoblado === 'TODOS') {
      this.model['cpoblado'] = {cod: 'TODOS', nombre: paramCpoblado};
    } else {
      this.model['cpoblado'] = {cod: idCpoblado, nombre: paramCpoblado};
    }
  }

  // enviar valores al padre
  sendDataParent() {
    // console.log('model departamento hpta! --> ', this.model['depto']);
    const idEmpresa = this.suiEmpresas.find(empresa => this.selectEmpresa === empresa.nombre).id_empresa;
    const codServicio = this.suiEmpresas.find(empresa => this.selectEmpresa === empresa.nombre).cod_servicio;
    const nombreServicio = this.suiEmpresas.find(empresa => this.selectEmpresa === empresa.nombre).servicio;
    // tslint:disable-next-line: max-line-length
    this.model['empresa'] = {cod_empresa: idEmpresa, nombre: this.selectEmpresa, cod_servicio: codServicio, servicio: nombreServicio };
    if (!this.selectDpto) {
      // console.log('Seleccion depto --> ', this.selectDpto);
      this.model['depto'] = {cod: 'TODOS', nombre: 'TODOS'};
      this.model['mpio'] = {cod: 'TODOS', nombre: 'TODOS'};
      this.model['cpoblado'] = {cod: 'TODOS', nombre: 'TODOS'};
    }
    const data = { modal: 'empresa', value: this.model };
    this.dialogRef.close(data);
  }
}
