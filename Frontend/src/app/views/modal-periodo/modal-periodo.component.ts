import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MomentDateAdapter, MAT_MOMENT_DATE_ADAPTER_OPTIONS } from '@angular/material-moment-adapter';
import { MAT_DATE_LOCALE, DateAdapter, MAT_DATE_FORMATS } from '@angular/material/core';
import { MatDatepicker } from '@angular/material/datepicker';
import { MatDialogRef } from '@angular/material/dialog';
import * as moment from 'moment';
import { Moment } from 'moment';
import { MY_FORMATS } from 'src/app/constants/constants';
import { ISUIError } from 'src/app/models/IOptionsMapa.model';
import { AppObservableService } from 'src/app/services/app-observable.service';
import { SuiService } from 'src/app/services/sui.service';

@Component({
  selector: 'app-modal-periodo',
  templateUrl: './modal-periodo.component.html',
  styleUrls: ['./modal-periodo.component.scss'],
  providers: [
    {provide: MAT_DATE_LOCALE, useValue: 'es-ES'}, // Permite ver el calendario en español
    {
      provide: DateAdapter,
      useClass: MomentDateAdapter,
      deps: [MAT_DATE_LOCALE, MAT_MOMENT_DATE_ADAPTER_OPTIONS],
    },
    {provide: MAT_DATE_FORMATS, useValue: MY_FORMATS},
  ],
})
export class ModalPeriodoComponent implements OnInit {

  selectAnio: number;
  selectMes: number = null;
  suiAnios: any[] = null;
  date = new FormControl(moment());
  startDate: Date;

  constructor(
    private formBuilder: FormBuilder,
    private suiService: SuiService,
    public observer: AppObservableService,
    private dialogRef: MatDialogRef<ModalPeriodoComponent>,
  ) { }

  optionsMap = this.formBuilder.group({
    anio: [null, Validators.required],
    mes: null,
  });

  ngOnInit(): void {
    this.loadSuiAnios();
    const loadData = JSON.parse(localStorage.getItem('periodo'));
    if (loadData) {
      // console.log('loadData -> ', loadData);
      this.selectAnio = loadData.anio;
      this.optionsMap.get('mes').setValue(moment(loadData.mes));
      const mes = this.optionsMap.get('mes').value.format('M') - 1;
      this.startDate = new Date(loadData.anio, mes, 1); // Actualizar año y mes seleccionado en el modal de meses
    } else {
      const fecha = new Date();
      this.selectAnio = fecha.getFullYear() - 2;
      const ctrlDate = this.date.value;
      ctrlDate.month(this.selectMes - 5);
      this.optionsMap.get('mes').setValue(ctrlDate);
    }
  }

  // enviar valores al padre
  sendDataParent() {
    this.optionsMap.value['label'] = this.convertDateLabel(`${moment(this.optionsMap.value['mes']).locale('es').format('MMMM')} - ${this.optionsMap.value['anio']}`);
    this.optionsMap.value['mes'] = moment(this.optionsMap.value['mes']).locale('es').format('M');
    const data = {modal: 'periodo', value: this.optionsMap.value};
    this.dialogRef.close(data);
  }

  convertDateLabel(fecha) {
    const label = fecha.charAt(0).toUpperCase() + fecha.slice(1);
    return label;
  }

  // Se hace llamado al servicio para cargar años
  loadSuiAnios() {
    this.suiService.getAnios().subscribe( anios => {
      this.suiAnios = anios;
      // console.log(this.suiAnios);
    }, (error: ISUIError) => {
      // console.log(error);
      this.observer.setShowAlertErrorSUI(error.status);
    });
  }

  // se ejecuta cuando se cambien valores del año
  somethingChanged(select: any): void {
    const mesActual = this.optionsMap.get('mes').value.format('M') - 1;
    this.startDate = new Date(select, mesActual, 1); // Actualizar año y mes seleccionado en el modal de meses
  }

  chosenYearHandler(normalizedYear: Moment) {
    const ctrlValue = this.optionsMap.get('mes').value;
    ctrlValue.year(normalizedYear.year());
    this.optionsMap.get('mes').setValue(ctrlValue);
  }

  // permite actualizar el modal de fechas
  chosenMonthHandler(normalizedMonth: Moment, datepicker: MatDatepicker<Moment>) {
    const ctrlValue = this.date.value;
    ctrlValue.month(normalizedMonth.month());
    this.optionsMap.get('mes').setValue(ctrlValue);
    this.startDate = new Date(this.selectAnio, ctrlValue.format('M') - 1, 1); // Actualizar año y mes seleccionado en el modal de meses
    datepicker.close();
  }

}
