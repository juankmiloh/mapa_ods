import { Component, OnInit, ViewChild, ElementRef, OnDestroy } from '@angular/core';
import { setDefaultOptions, loadModules, loadCss } from 'esri-loader';
import { IOptionsMapa } from 'src/app/models/IOptionsMapa.model';
import * as d3 from 'd3';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppObservableService } from '../../services/app-observable.service';
import { SwalComponent } from '@sweetalert2/ngx-sweetalert2';
import { ISUIError, ICausas } from '../../models/IOptionsMapa.model';
import { SuiService } from 'src/app/services/sui.service';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-map-interrupcion',
  templateUrl: './map-interrupcion.component.html',
  styleUrls: ['./map-interrupcion.component.scss'],
})
export class MapInterrupcionComponent implements OnInit, OnDestroy {
  periodo = null;
  empresa = null;
  legend: any;

  constructor(
    private snackBar: MatSnackBar,
    public observer: AppObservableService,
    private suiService: SuiService,
  ) {}

  // The <div> where we will place the map
  @ViewChild('mapViewNode', { static: true }) private mapViewEl: ElementRef;
  @ViewChild('alertSwal', { static: true }) private alertSwal: SwalComponent;

  public view: any;
  serverUrl = environment.serverUrl;
  errorMessage = '';
  // Controla el CSS del Backdrop
  fbbackMap = 'fbback_map_hide';
  fbbackMapLoad = 'fbback_map_show_load';
  // Permite controlar el backdrop cuando se cambia el CSV
  updateLayerCSV = true;
  // guarda los valores del CSV consultado
  dataCSV: any;
  optionsSwal: any;
  AlertErrorSUI: number;
  // interface de opciones del mapa
  options: IOptionsMapa;
  meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
  // opciones del progress de carga
  mode: ProgressSpinnerMode = 'determinate';
  value = 50;

  async ngOnInit() {
    this.validateChangePeriodo();
    this.validateChangeBasemap();
    this.validateChangeEmpresa();
    // Validar conexion SUI
    await this.verifyConnectionSUI().then((data: any) => {
      // console.log('estado servidor: ', data);
      if (data.status !== undefined) {
        this.observer.setShowAlertErrorSUI(data.status);
      }
    });
    this.validateConnectionSUI();

    // Initialize MapView and return an instance of MapView
    const fecha = new Date();
    const anoActual = fecha.getFullYear() - 1;
    // const mesActual = fecha.getMonth(); // Trae el mes anterior al actual
    const mesActual = 3; // prueba
    // console.log('MES ACTUAL: ', mesActual);
    // opciones iniciales del mapa a visualizar
    this.options = {
      ano: anoActual,
      mes: mesActual,
      empresa: 2249,
      nombEmpresa: 'Todas las empresas',
      causa: 0,
      colSui: 'Todas',
      nombCausa: 'Todas',
      zoom: 4,
      latitud: 2.5,
      longitud: -73.47106040285713,
    };

    await this.initializeMap(this.options).then(mapView => {});
  }

  // observable para validar si hay error en la conexion con la BD SUI
  validateConnectionSUI() {
    this.observer.getShowAlertErrorSUI().subscribe((status) => {
      console.log('status servidor: ', status);
      // Si no hay conexion con el servidor
      if (status === 0) {
        this.alertSwal.swalOptions = {
          title: 'Error',
          text: 'No hay conexión con el servidor',
          icon: 'error',
          // showCancelButton: true,
          // cancelButtonColor: '#e91e63',
          confirmButtonText: 'Contactar al administrador',
          confirmButtonColor: '#3f51b5',
          allowOutsideClick: false,
        };

        this.alertSwal.fire().then((data) => {
          if (data.value) {
            window.location.href = 'https://wa.link/2zk6io';
          }
        });
      }

      // Error interno del servidor
      if (status === 500) {
        this.alertSwal.swalOptions = {
          title: 'Info',
          text: 'Se ha perdido la conexión con el servidor',
          icon: 'info',
          confirmButtonText: 'Recargar Página',
          confirmButtonColor: '#ffa726',
          allowOutsideClick: false,
        };

        if (!this.alertSwal.swalVisible) { // si el modal no esta abierto
          this.alertSwal.fire().then((data) => {
            if (data.value) {
              window.location.reload();
            }
          });
        }
      }
    });
  }

  // Observable que permite controlar el cambio de basemap (claro | oscuro)
  validateChangeBasemap() {
    this.observer.getChangeBasemap().subscribe((status) => {
      // console.log('Status observable basemap --> ', status);
      const basemap = this.view.map.basemap.id;
      this.showBackdrop('fbback_map_show_load');
      if (status === 'oscuro' && basemap === 'streets-night-vector') {
        this.view.map.basemap = 'streets-navigation-vector'; // Cambiar el baseMap a Claro
        this.openSnackBar(`Modo claro activado`, null);
      } else {
        this.view.map.basemap = 'streets-night-vector'; // Cambiar el baseMap a Oscuro
        this.openSnackBar(`Modo oscuro activado`, null);
      }
    });
  }

  // Observable que permite controlar el cambio de periodo (año | mes)
  validateChangePeriodo() {
    this.observer.getChangePeriodo().subscribe((status) => {
      console.log('Status observable periodo --> ', this.empresa);
      this.periodo = status;
      if (this.empresa !== null) {
        const options = {
          ano: status.anio,
          mes: status.mes,
          empresa: this.empresa,
          nombEmpresa: 'Todas las empresas',
          causa: 0,
          colSui: 'Todas',
          nombCausa: 'Todas',
          zoom: 4,
          latitud: 2.5,
          longitud: -73.47106040285713,
        };
        this.addLayer(options).then((data) => {
          this.view.map.layers = data; // Se agrega un nuevo layer CSV al mapa
        });
      } else {
        // this.alertSwal.swalOptions = {
        //   title: 'Info',
        //   text: 'Seleccione una empresa',
        //   icon: 'info',
        //   allowOutsideClick: false,
        // };
        // this.alertSwal.fire();
      }
    });
  }

  // Observable que permite controlar el cambio de empresa (año | mes)
  validateChangeEmpresa() {
    this.observer.getChangeEmpresa().subscribe((status) => {
      console.log('Status observable empresa --> ', this.periodo);
      this.empresa = status.cod_empresa;
      if (this.periodo) {
        const options = {
          ano: this.periodo.anio,
          mes: this.periodo.mes,
          empresa: status.cod_empresa,
          nombEmpresa: 'Todas las empresas',
          causa: 0,
          colSui: 'Todas',
          nombCausa: 'Todas',
          zoom: 4,
          latitud: 2.5,
          longitud: -73.47106040285713,
        };
        this.addLayer(options).then((data) => {
          this.view.map.layers = data; // Se agrega un nuevo layer CSV al mapa
        });
      } else {
        // this.alertSwal.swalOptions = {
        //   title: 'Info',
        //   text: 'Seleccione un período',
        //   icon: 'info',
        //   allowOutsideClick: false,
        // };
        // this.alertSwal.fire();
      }
    });
  }

  ngOnDestroy() {
    if (this.view) {
      this.view.container = null; // destroy the map view
    }
  }

  // Mostrar mensaje flotante en el footer de la pagina
  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: 2000,
      horizontalPosition: 'right',
      verticalPosition: 'bottom',
    });
  }

  // Mostrar Backdrop
  showBackdrop(cssLoad: string): void {
    // console.log('showBackdrop');
    this.fbbackMap = 'fbback_map_init';
    this.fbbackMapLoad = cssLoad;
    this.view.popup.close(); // Se cierran los popups del mapa
  }

  // Ocultar Backdrop
  hideBackdrop(): void {
    // console.log('hideBackdrop');
    this.fbbackMap = 'fbback_map_hide';
  }

  // Se carga el mapa
  async initializeMap(options: IOptionsMapa) {
    setDefaultOptions({ version: '4.12' }); // Se configura la version del API de ARCgis a utilizar
    loadCss('4.12'); // Se cargan los estilos de la version a utilizar

    try {
      // Load the modules for the ArcGIS API for JavaScript
      // tslint:disable-next-line: max-line-length
      const [Track, Map, MapView, Search, Legend, BasemapToggle, watchUtils] = await loadModules(['esri/widgets/Track', 'esri/Map', 'esri/views/MapView', 'esri/widgets/Search', 'esri/widgets/Legend', 'esri/widgets/BasemapToggle', 'esri/core/watchUtils']);

      // Configure the Map
      const mapProperties = {
        basemap: 'streets-navigation-vector',
      };

      const map = new Map(mapProperties);

      // Initialize the MapView
      const mapViewProperties = {
        container: this.mapViewEl.nativeElement,
        center: [options.longitud, options.latitud], // [horizontal (long), vertical (lat)]
        zoom: options.zoom,
        constraints: {
          minZoom: 3,
          maxZoom: 19,
          snapToZoom: true,
         },
        map,
      };

      this.view = new MapView(mapViewProperties);

      // Mostrar backDrop de carga mientras se inicia la vista
      watchUtils.whenOnce(this.view, 'ready').then(() => {
        this.showBackdrop('fbback_map_show_load');
      });

      // Display the loading indicator when the view is updating
      watchUtils.whenTrue(this.view, 'updating', (evt: any) => {
        // console.log('showLoad', evt);
        watchUtils.whenTrue(this.view, 'stationary', () => {
          // Get the new extent of view/map whenever map is updated.
          if (this.view.extent) {
            if (this.updateLayerCSV) {
              this.showBackdrop('fbback_map_show_load');
            }
          }
        });
      });

      // Hide the loading indicator when the view stops updating
      watchUtils.whenFalse(this.view, 'updating', (evt: any) => {
        // console.log('closeLoad', evt);
        if (this.updateLayerCSV) {
          this.openSnackBar('Datos actualizados correctamente.', null);
          this.snackBar._openedSnackBarRef.afterOpened().subscribe(async (data) => {
            this.updateLayerCSV = false;
          });
        }
        this.fbbackMap = 'fbback_map_hide';
        watchUtils.whenTrue(this.view.popup, 'visible', (evt1: any) => {
          // console.log('show POPUP!', evt1);
        });
      });

      this.legend = new Legend({ view: this.view });
      const search = new Search({ view: this.view });
      const basemapToggle = new BasemapToggle({ view: this.view });
      const track = new Track({ view: this.view });

      this.view.ui.add(search, { position: 'top-right' });    // Muestra el input de busqueda
      this.view.ui.remove([basemapToggle, 'zoom']);           // Elimina los botones de zoom
      this.view.ui.add(track, 'top-right');                   // Muestra el boton de MyLocation

      // this.view.map.layers = await this.addLayer(options);

      return this.view;

    } catch (error) {
      // console.log('EsriLoader: ', error);
    }
  }

  async addLayer(options) {
    // console.log('OPTIONS: ', options);
    this.updateLayerCSV = true;
    this.legend.style = { type: 'card', layout: 'side-by-side' }; // CSS leyenda tipo card

    this.view.ui.add(this.legend, { position: 'bottom-left' });  // Muestra las convenciones del mapa

    const [CSVLayer] = await loadModules(['esri/layers/CSVLayer']);
    const urlOptions = `${this.serverUrl}/i_interrupcion/${options.ano}/${options.mes}/${options.empresa}/${options.causa}`;
    // const urlOptions = 'assets/file_interrupciones1.csv';
    console.log(urlOptions);
    this.dataCSV = d3.csv(urlOptions);

    // Validación para saber si existen datos de vuelta de la URL
    this.dataCSV.then((data: ICausas) => {
      console.log('DATA CSV -> ', data);
      if (data.length === 0) {
        this.alertSwal.swalOptions = {
          text: 'No hay interupciones para este período.',
          icon: 'info',
          confirmButtonText: 'Aceptar',
          confirmButtonColor: '#ffa726',
          allowOutsideClick: true,
        };
        this.alertSwal.fire();
      }
    });

    try {
      // Paste the url into a browser's address bar to download and view the attributes
      // in the CSV file. These attributes include:
      // * centro_poblado - nombre municipio
      // * longitude - longitud municipio
      // * latitude - latitud municipio
      // * cod_dane - codigo dane municipio
      // * cod_empresa - empresa del municipio
      // * total - total de horas de interrupciones

      const template = {
        // tslint:disable-next-line: max-line-length
        title:  '<div style="border: 0px solid black; background: #e3f2fd; width: 15em; border-radius: 5px; height: 4em; padding-top: 0.3em;">' +
                '  <small style="color: #3f51b5;"><b>{centro_poblado}</b></small><br>' +
                '  <small style="color: #212121; padding-left: 3%;">Horas de interrupción {total}</small>' +
                '</div>',
        content: '<div>' +
                 ' <small>Código DANE municipio {cod_dane}</small><br>' +
                 ` <small><u>{nom_empresa}</u> código {cod_empresa}</small><br>` +
                 ` <small>Interrupciones <u>${options.nombCausa.toUpperCase()}</u> para <u>${this.meses[options.mes].toUpperCase()}</u> de <u>${options.ano}</u></small>` +
                 '</div>',
      };

      // The heatmap renderer assigns each pixel in the view with
      // an intensity value. The ratio of that intensity value
      // to the maxPixel intensity is used to assign a color
      // from the continuous color ramp in the colorStops property
      const renderer = {
        type: 'heatmap',
        field: `total`,
        colorStops: [
          { color: 'rgba(63, 40, 102, 0)', ratio: 0 }, // rango de 0 a 1
          { color: '#6300df', ratio: 0.083 },          // Azul claro
          { color: '#2196f3', ratio: 0.100 },          // Azul
          { color: '#00ff2c', ratio: 0.166 },          // Verde Clarito
          { color: '#a1ff00', ratio: 0.249 },          // Verde
          { color: '#e5ff00', ratio: 0.332 },          // Amarillo claro
          { color: '#ffeb3b', ratio: 0.415 },          // Amarillo
          { color: '#ffc700', ratio: 0.498 },          // Amarillo oscuro
          { color: '#fea701', ratio: 0.581 },          // Naranja claro
          { color: '#ff9800', ratio: 0.664 },          // Naranja
          { color: '#f44336', ratio: 1 },               // Rojo
        ],
        minPixelIntensity: 0,
        maxPixelIntensity: 50000,
      };

      const layer = new CSVLayer({
        url: urlOptions,
        title: `Interrupciones ${options.colSui} ${this.meses[options.mes]} de ${options.ano}`,
        // title: `Mapa ODS`,
        copyright: 'DESARROLLADO POR JUAN CAMILO HERRERA - SUPERSERVICIOS',
        popupTemplate: template,
        renderer,
      });

      this.options = options; // Actualiza los valores seleccionados en modal OPTIONS

      return layer;
    } catch (error) {
      // console.log('EsriLoader: ', error);
    }
  }

  async verifyConnectionSUI() {
    const result = this.suiService.verifyConnectionSUI();
    return result;
  }
}
