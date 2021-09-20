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
  public suiEmpresas: any[] = [];
  loadEmpresas = false;

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
  }

  optionsMap = this.formBuilder.group({
    empresa: [null, Validators.required],
  });
  filteredEmpresas: Observable<IEmpresa[]>;

  ngOnInit(): void {
    this.loadEmpresas = true;
    this.loadSuiEmpresas();
  }

  // Se hace llamado al servicio para cargar empresas
  loadSuiEmpresas() {
    this.suiService.getEmpresas().subscribe(empresas => {
      this.suiEmpresas = empresas;
      this.suiEmpresas.unshift({
        cod_empresa: 0,
        nombre: 'TODAS',
        servicio: 'ENERGIA',
      });
      this.selectEmpresa = 'TODAS';
      this.loadEmpresas = false;
      // Se cargan los datos si ya habido una empresa seleccionada
      const loadData = JSON.parse(localStorage.getItem('empresa'));
      if (loadData) {
        this.selectEmpresa = loadData.nombre;
        console.log(this.selectEmpresa);
      }
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
    const codEmpresa = this.suiEmpresas.find(empresa => this.selectEmpresa === empresa.nombre).cod_empresa;
    const servicio = this.suiEmpresas.find(empresa => this.selectEmpresa === empresa.nombre).servicio;
    const model = {cod_empresa: codEmpresa, nombre: this.selectEmpresa, servicio };
    const data = { modal: 'empresa', value: model };
    this.dialogRef.close(data);
  }
}
