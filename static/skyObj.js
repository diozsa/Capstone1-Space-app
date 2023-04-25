// The Messier catalog - an array of objects with name and ID properties
const skyObject = [
  { name: 'The Crab Nebula', id: 'm1' },
  { name: 'Globular Cluster', id: 'm2' },
  { name: 'The Lagoon Nebula', id: 'm8' },
  { name: 'The Eagle Nebula', id: 'm16' },
  { name: 'The Omega Nebula', id: 'm17' },
  { name: 'Trifid Nebula', id: 'm20' },
  { name: 'The Sagittarius Star Cloud', id: 'm24' },
  { name: 'Dumbbell Nebula', id: 'm27' },
  { name: 'The Andromeda Galaxy', id: 'm31' },
  { name: 'Elliptical Galaxy', id: 'm32' },
  { name: 'Triangulum Galaxy', id: 'm33' },
  { name: 'Binary Star', id: 'm40' },
  { name: 'The Orion Nebula', id: 'm42' },
  { name: 'Emission Nebula', id: 'm43' },
  { name: 'The Beehive Cluster', id: 'm44' },
  { name: 'The Pleiades Cluster', id: 'm45' },
  { name: 'The Whirlpool Galaxy', id: 'm51' },
  { name: 'The Ring Nebula', id: 'm57' },
  { name: 'Spiral Galaxy', id: 'm58' },
  { name: 'The Sunflower Galaxy', id: 'm63' },
  { name: 'Cetus', id: 'm77' },
  { name: 'Diffuse Nebula', id: 'm78' },
  { name: 'The Cigar Galaxy', id: 'm82' },
  { name: 'The Southern Pinwheel Galaxy', id: 'm83' },
  { name: 'Lenticular Galaxy', id: 'm84' },
  { name: 'Planetary Nebula', id: 'm97' },
  { name: 'The Pinwheel Galaxy', id: 'm101' },
  { name: 'The Sombrero Galaxy', id: 'm104' },
  { name: 'The Heart Nebula', id: 'ic1805' },
  { name: 'Barred Spiral Galaxy', id: 'ngc1300' },
  { name: 'California Nebula', id: 'ngc1499' },
  { name: 'The Butterfly Nebula', id: 'ngc6302' },
  { name: 'Helix Nebula', id: 'ngc7293' },
  { name: 'Supernova', id: 'supernova' },
  { name: 'Cat Eye Nebula', id: 'ngc6543' },
  { name: 'Star Formation', id: 'formation' },
  { name: 'Horsehead Nebula', id: 'barnard33' },
  { name: 'Green Nebula', id: 'rcw120' },
  { name: 'Magellanic Clouds', id: 'mc' },
  { name: 'Europa', id: 'europa' },
  { name: 'The Great Red Spot', id: 'jupiter_spot' },
  { name: 'The Sun', id: 'sun' },
  { name: 'Mercury', id: 'mercury' },
  { name: 'Venus', id: 'venus' },
  { name: 'Mars', id: 'mars' },
  { name: 'Jupiter', id: 'jupiter' },
  { name: 'Saturn', id: 'saturn' },
  { name: 'Uranus', id: 'uranus' },
  { name: 'Neptune', id: 'neptune' },
  { name: 'Pluto', id: 'pluto' }
];

function fillRandomObject() {
  // Select a random object from the catalog
  const randomIndex = Math.floor(Math.random() * skyObject.length);
  const randomObject = skyObject[randomIndex];

  // Fill the search field with the object's name and submit the form
  const searchField = document.getElementById('search');
  console.log(searchField);
  searchField.value = randomObject.name;
  document.getElementById('search-form').submit();
}