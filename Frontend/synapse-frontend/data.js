export const companies = [
  "Volkswagen AG",
  "AkzoNobelNV",
  "Brenntag",
  "Continental AG",
  "Zalando SE",
  "Vonovia SE",
  "Siemens AG",
  "Adidas AG"
];

export const queries = [
  "Air Emissions", 
  "Business Ethics",
  "Community and Society",
  "Human Rights",
  "Environmental Management",
  "Sustainable Production",
  "Biodiversity",
  "Supply Chain"
];

export const form_dropdowns = [
  {
    label: "Company",
    placeholder : "Select Company",
    options : companies
  },
  {
    label: "Query",
    placeholder : "Select Query",
    options : queries
  }
]

export const stages = [
      { status: 'Parsing query...', duration: 2000 },
      { status: 'Retrieving evidence from sources...', duration: 2000 },
      { status: 'Analyzing sustainability claims...', duration: 2000 },
      { status: 'Generating explanation...', duration: 2000 },
    ];