export const MY_FORMATS = {
    parse: {
        dateInput: 'MMMM',
    },
    display: {
        dateInput: 'MMMM',
        monthYearLabel: 'MMM',
    },
};

export const LIST_SIDENAV = [
    {
        name: 'divider',
    },
    {
        name: 'subheader',
        header: 'Configuración',
    },
    {
        name: 'Servicio',
        icon: 'roofing',
        select: '',
    },
    {
        name: 'Capa',
        icon: 'layers',
        select: '',
    },
    {
        name: 'Período',
        icon: 'event',
        select: '',
        hidden: true,
    },
    {
        name: 'Empresa',
        icon: 'corporate_fare',
        hidden: true,
    },
    {
        name: 'divider',
    },
    {
        name: 'subheader',
        header: 'Herramientas',
    },
    {
        name: 'Modo oscuro',
        icon: 'nightlight_round',
    },
    {
        name: 'Estadísticas',
        icon: 'assessment',
        hidden: true,
    },
    // {
    //     name: 'divider',
    // },
    // {
    //     name: 'Usuarios',
    //     icon: 'people_alt',
    // },
    {
        name: 'Visitas',
        icon: 'people_alt',
        select: ''
    },
    {
        name: 'divider',
    },
    {
        name: 'Acerca de SSPD - ODS',
        icon: 'help_outline',
    },
];
