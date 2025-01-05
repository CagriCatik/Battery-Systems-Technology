// sidebars.js

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // Main Tutorial Sidebar
  tutorialSidebar: [

    // ==============================================
    // Fundamentals Category
    {
      type: 'category',
      label: 'Fundamentals',
      items: [
        'Fundamentals/introduction',
        'Fundamentals/components',
        'Fundamentals/em-asm',
        'Fundamentals/em-pmsm',
        'Fundamentals/pe',
      ],
    },

    // ==============================================
    // Battery Category
    {
      type: 'category',
      label: 'Battery',
      items: [
        'Battery/why_lithium_battery',
        'Battery/form_factors',
        'Battery/battery_terminology',
        // Add more battery-related docs here
      ],
    },

    // ==============================================
    // Advanced Concepts Category
    {
      type: 'category',
      label: 'Advanced Concepts',
      items: [
        'Advanced-Concepts/ocv_vs_soc',
        'Advanced-Concepts/specification_sheet',
        'Advanced-Concepts/sizing_basics',
        'Advanced-Concepts/soa_lithium',
        'Advanced-Concepts/battery_standards',
      ],
    },

    // ==============================================
    // System and Algorithms Category
    {
      type: 'category',
      label: 'System and Algorithms',
      items: [
        'System_and_Algorithms/introduction',
        'System_and_Algorithms/function_of_bms',
        'System_and_Algorithms/bms_algorithm',
        'System_and_Algorithms/soh_estimation',
        'System_and_Algorithms/cycle_counting',
        'System_and_Algorithms/soh_algorithm',
        'System_and_Algorithms/cell_balancing',
        'System_and_Algorithms/balancing_methods',
        'System_and_Algorithms/advanced_balancing',
        'System_and_Algorithms/bms_architecture',
        'System_and_Algorithms/state_machine',
        'System_and_Algorithms/control_systems',
        'System_and_Algorithms/development_trends',

      ],
    },
    // ==============================================
    // Modeling and Design
    {
      type: 'category',
      label: 'Modeling and Desing',
      items: [
        'Modeling_Design/soc_soh_estimation',
        'Modeling_Design/matlab_design',
        'Modeling_Design/equivalent_models',
        'Modeling_Design/diffusion_voltage',

      ],
    },

    // ==============================================
    // Glossary Category
    {
      type: 'category',
      label: 'Glossary',
      items: [
        'Glossary/A',
        'Glossary/B',
        'Glossary/C',
        'Glossary/D',
        'Glossary/E',
        'Glossary/F',
        'Glossary/G',
        'Glossary/H',
        'Glossary/I',
        'Glossary/J',
        'Glossary/K',
        'Glossary/L',
        'Glossary/M',
        'Glossary/N',
        'Glossary/O',
        'Glossary/P',
        'Glossary/Q',
        'Glossary/R',
        'Glossary/S',
        'Glossary/T',
        'Glossary/U',
        'Glossary/V',
        'Glossary/W',
        'Glossary/X',
        'Glossary/Y',
        'Glossary/Z',
      ],
    },

    // ==============================================
    // Any other custom items can be added here
  ],

  // ==============================================
  // Codes Sidebar with Custom Elements
  codesSidebar: [
  
    // Rust
    {
      type: 'category',
      label: 'Rust',
      items: [
        'codes/rust/btms',
        'codes/python/example',
      ],
    },

    // Python 
    {
      type: 'category',
      label: 'Python',
      items: [
        'codes/python/btms',
        'codes/python/example',
      ],
    },

    // MATLAB 
    {
      type: 'category',
      label: 'MATLAB',
      items: [
        'codes/python/btms',
        'codes/python/example',
      ],
    },
  ],

  // You can define more sidebars here if needed
};

export default sidebars;
