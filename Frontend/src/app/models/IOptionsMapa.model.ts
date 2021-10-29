export interface IOptionsMapa {
  zoom?: number;
  latitud?: number;
  longitud?: number;
  servicio?: number;
  ano?: number;
  mes?: number;
  empresa?: number;
  sector?: number;
  dpto?: number;
  mpio?: number;
  cpoblado?: number;
}

export interface IDialogData {
  view: any;
  fabOptions: any;
  optionsMap: IOptionsMapa;
  suiAnios: number;
  suiCausas: any;
  suiEmpresas: any;
  updateLayerCSV: boolean;
  dataCSV: any;
}

export interface IEmpresa {
  cod_empresa: number;
  nombre: string;
  servicio: string;
}

export interface ICausas {
  calzesp: number;
  castnat: number;
  centro_poblado: string;
  cod_dane: string;
  cod_empresa: string;
  exp: number;
  fnivel1: number;
  infra: number;
  latitude: number;
  longitude: number;
  nom_empresa: string;
  npnexc: number;
  pnexc: number;
  remer: number;
  segciu: number;
  stnstr: number;
  sumi: number;
  terr: number;
  total: number;
  tsubest: number;
  length?: number;
}

export interface ICausa {
  causa: string;
  descripcion?: string;
  horas_interrupcion: number;
}

export interface ISUIError {
  status: number;
  message: number;
}

export interface Section {
  name: string;
  icon?: string;
  header?: string;
  select?: string;
}

export interface IOptionsEmrepsa {
  empresa: {cod_empresa: number, nombre: string, cod_servicio: number, servicio: string};
  depto: {cod: any, nombre: any};
  mpio: {cod: any, nombre: any};
  cpoblado: {cod: any, nombre: any};
}

export const modelEmpresa = {
  empresa: {cod_empresa: null, nombre: null, cod_servicio: null, servicio: null},
  depto: {cod: 'TODOS', nombre: 'TODOS'},
  mpio: {cod: 'TODOS', nombre: 'TODOS'},
  cpoblado: {cod: 'TODOS', nombre: 'TODOS'},
};
