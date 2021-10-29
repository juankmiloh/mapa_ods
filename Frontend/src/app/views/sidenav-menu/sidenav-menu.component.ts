import { Component, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSelectionList } from '@angular/material/list';
import { LIST_SIDENAV } from 'src/app/constants/constants';
import { Section } from 'src/app/models/IOptionsMapa.model';
import { AppObservableService } from 'src/app/services/app-observable.service';
import { ModalCapasComponent } from '../modal-capas/modal-capas.component';
import { ModalEmpresaComponent } from '../modal-empresa/modal-empresa.component';
import { ModalPeriodoComponent } from '../modal-periodo/modal-periodo.component';
import { ModalServicioComponent } from '../modal-servicio/modal-servicio.component';

@Component({
  selector: 'app-sidenav-menu',
  templateUrl: './sidenav-menu.component.html',
  styleUrls: ['./sidenav-menu.component.scss'],
})
export class SidenavMenuComponent {
  x: any;
  myWindow: Window;
  options: Section[] = LIST_SIDENAV;
  showFiller = false;
  depto: any;
  mpio: any;
  cpoblado: any;
  usuariosConsumo: string;

  constructor(
    public dialog: MatDialog,
    public observer: AppObservableService,
  ) {}

  @ViewChild('items') listSidenav: MatSelectionList;

  empresa = 'OBJETIVOS DE DESARROLLO SOSTENIBLE';

  ngOnInit() {
    this.x = window.matchMedia('(max-width: 800px)'); // Si hace match con dispositivos móviles
    // this.listSidenav.deselectAll();
    localStorage.removeItem('servicio');
    localStorage.removeItem('periodo');
    localStorage.removeItem('capas');
    localStorage.removeItem('empresa');
  }

  close(reason: string) {}

  // mostrar modal
  openDialog(option): void {
    // console.log('Abrir modal --> ', option);
    let modal: any
    if (option.name === 'Servicio') {
      modal = ModalServicioComponent
      this.listSidenav.deselectAll();
    } else if (option.name === 'Período') {
      modal = ModalPeriodoComponent
      this.listSidenav.deselectAll();
    } else if (option.name === 'Empresa') {
      modal = ModalEmpresaComponent
      this.listSidenav.deselectAll();
    } else if (option.name === 'Capa') {
      modal = ModalCapasComponent
      this.listSidenav.deselectAll();
    } else if (option.name === 'Modo oscuro') {
      this.options[8].name = 'Modo claro';
      this.options[8].icon = 'light_mode';
      this.listSidenav.deselectAll();
      this.observer.setChangeBasemap('claro');
    } else if (option.name === 'Modo claro') {
      this.options[8].name = 'Modo oscuro';
      this.options[8].icon = 'nightlight_round';
      this.listSidenav.deselectAll();
      this.observer.setChangeBasemap('oscuro');
    } else {
      return;
    }

    // Si la opcion seleccionada abre algun modal
    if (modal) {
      const dialogRef = this.dialog.open(modal, {
        closeOnNavigation: true,
        maxWidth: this.x.matches ? '90%' : '60%',
        // height: this.x.matches ? '100%' : '',
        disableClose: false,
        data: {},
      });

      // Acciones luego de cerrar el modal
      dialogRef.afterClosed().subscribe((dataFromModal) => {
        // console.log('The dialog was closed', dataFromModal);
        if (dataFromModal) {
          if (dataFromModal.modal === 'servicio') {
            const loadData = JSON.parse(localStorage.getItem('servicio'));
            if (loadData) {
              if (loadData.cod_servicio !== dataFromModal.value.cod_servicio) {
                localStorage.removeItem('empresa');
                this.observer.setChangeServicio('updateMap');
                this.empresa = 'OBJETIVOS DE DESARROLLO SOSTENIBLE';
                this.depto = null;
                this.mpio = null;
                this.cpoblado = null;
              } else {
                const dataEmpresa = localStorage.getItem('empresa');
                if (dataEmpresa) {
                  this.observer.setChangeServicio(dataFromModal.value.cod_servicio);
                }
              }
            }
            localStorage.setItem('servicio', JSON.stringify(dataFromModal.value));
            this.options[2].select = dataFromModal.value['servicio'];
          } else if (dataFromModal.modal === 'capas') {
            localStorage.setItem('capas', JSON.stringify(dataFromModal.value));
            this.options[3].select = dataFromModal.value.capa; // Se muestra msj de la opcion seleccionada
            this.usuariosConsumo = dataFromModal.value.option.nombre;
            this.options[4]['hidden'] = false; // Se habilita en la lista del menu LATERAL la opcion de PERIODO
            this.observer.setChangeSector(dataFromModal.value);
          } else if (dataFromModal.modal === 'periodo') {
            localStorage.setItem('periodo', JSON.stringify(dataFromModal.value));
            this.observer.setChangePeriodo(dataFromModal.value);
            this.options[4].select = dataFromModal.value.label; // Se muestra msj de la opcion seleccionada
            this.options[5]['hidden'] = false; // Se habilita en la lista del menu LATERAL la opcion de empresas
            this.listSidenav.deselectAll();
          } else if (dataFromModal.modal === 'empresa') {
            try {
              this.empresa = dataFromModal.value.empresa.nombre;
              this.depto = dataFromModal.value.depto.nombre;
              this.mpio = dataFromModal.value.mpio.nombre;
              this.cpoblado = dataFromModal.value.cpoblado.nombre;
            } catch (error) {
              console.log(error);
            }
            localStorage.setItem('empresa', JSON.stringify(dataFromModal.value));
            this.observer.setChangeEmpresa(dataFromModal.value);
          } else {
            return;
          }
        }
      });
    }

  }

}
