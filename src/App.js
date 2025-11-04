import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';

function App() {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Filter states
  const [deviceFilters, setDeviceFilters] = useState({
    iPhone: true,
    Android: true,
    Unknown: true
  });

  const [iphoneGenerationFilters, setIphoneGenerationFilters] = useState({
    '17': true,
    '16': true,
    '15': true,
    '14': true,
    'Older': true,
    'Unknown': true
  });

  // Sort state
  const [sortByPrice, setSortByPrice] = useState('none'); // 'none', 'asc', 'desc'

  // Function to extract numeric value from price string
  const extractPrice = (priceString) => {
    if (!priceString) return 0;
    // Remove all non-numeric characters except decimal points
    const numericValue = priceString.replace(/[^0-9.]/g, '');
    return parseFloat(numericValue) || 0;
  };

  useEffect(() => {
    fetch('/data.csv')
      .then(response => response.text())
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          complete: (results) => {
            setData(results.data);
            setFilteredData(results.data);
            setLoading(false);
          },
          error: (error) => {
            console.error('Error parsing CSV:', error);
            setLoading(false);
          }
        });
      })
      .catch(error => {
        console.error('Error fetching CSV:', error);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    // Apply filters whenever filter states or data changes
    let filtered = data;

    // Apply device type filters
    filtered = filtered.filter(item => {
      const model = (item.Model || '').toLowerCase();

      const isIPhone = model.includes('iphone') || model.includes('apple');
      const isAndroid = model.includes('galaxy') || model.includes('samsung') ||
                       model.includes('pixel') || model.includes('oneplus') ||
                       model.includes('nothing');
      const isUnknown = !isIPhone && !isAndroid;

      return (deviceFilters.iPhone && isIPhone) ||
             (deviceFilters.Android && isAndroid) ||
             (deviceFilters.Unknown && isUnknown);
    });

    // Apply iPhone generation filters if iPhone is selected
    if (deviceFilters.iPhone) {
      filtered = filtered.filter(item => {
        const model = (item.Model || '').toLowerCase();
        const isIPhone = model.includes('iphone');

        if (!isIPhone) return true; // Keep non-iPhone items

        // Determine iPhone generation
        let generation = 'Unknown';
        if (model.includes('iphone 17')) generation = '17';
        else if (model.includes('iphone 16')) generation = '16';
        else if (model.includes('iphone 15')) generation = '15';
        else if (model.includes('iphone 14')) generation = '14';
        else if (model.includes('iphone 13') || model.includes('iphone 12') ||
                 model.includes('iphone 11') || model.includes('iphone x') ||
                 model.includes('iphone se') || model.includes('iphone 8')) generation = 'Older';

        return iphoneGenerationFilters[generation];
      });
    }

    // Apply sorting
    if (sortByPrice !== 'none') {
      filtered.sort((a, b) => {
        const priceA = extractPrice(a.Price);
        const priceB = extractPrice(b.Price);
        return sortByPrice === 'asc' ? priceA - priceB : priceB - priceA;
      });
    }

    setFilteredData(filtered);
  }, [data, deviceFilters, iphoneGenerationFilters, sortByPrice]);

  // Function to check if a string is a URL
  const isUrl = (string) => {
    try {
      new URL(string);
      return true;
    } catch {
      return false;
    }
  };

  // Function to check if a string looks like a file path
  const isFilePath = (string) => {
    return string && (string.includes('/') || string.includes('\\') || string.startsWith('./'));
  };

  // Function to render cell content
  const renderCellContent = (value) => {
    if (!value || value.trim() === '') {
      return '';
    }

    // Check if it's a URL or file path
    if (isUrl(value) || isFilePath(value)) {
      return (
        <button
          onClick={() => {
            if (isUrl(value)) {
              window.open(value, '_blank');
            } else {
              console.log('View file:', value);
            }
          }}
          style={{
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            padding: '6px 12px',
            cursor: 'pointer',
            fontSize: '14px',
            transition: 'background-color 0.2s'
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#0056b3'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#007bff'}
        >
          View
        </button>
      );
    }

    return value;
  };

  // Toggle device filter
  const toggleDeviceFilter = (filter) => {
    setDeviceFilters(prev => ({
      ...prev,
      [filter]: !prev[filter]
    }));
  };

  // Toggle iPhone generation filter
  const toggleIphoneGenerationFilter = (filter) => {
    setIphoneGenerationFilters(prev => ({
      ...prev,
      [filter]: !prev[filter]
    }));
  };

  // Handle price column click for sorting
  const handlePriceSort = () => {
    setSortByPrice(prevSort => {
      if (prevSort === 'none') return 'asc';
      if (prevSort === 'asc') return 'desc';
      return 'none';
    });
  };

  // Get count for each filter
  const getFilterCounts = () => {
    const counts = {
      device: { iPhone: 0, Android: 0, Unknown: 0 },
      generations: { '17': 0, '16': 0, '15': 0, '14': 0, 'Older': 0, 'Unknown': 0 }
    };

    data.forEach(item => {
      const model = (item.Model || '').toLowerCase();

      const isIPhone = model.includes('iphone') || model.includes('apple');
      const isAndroid = model.includes('galaxy') || model.includes('samsung') ||
                       model.includes('pixel') || model.includes('oneplus') ||
                       model.includes('nothing');
      const isUnknown = !isIPhone && !isAndroid;

      // Count device types
      if (isIPhone) counts.device.iPhone++;
      else if (isAndroid) counts.device.Android++;
      else counts.device.Unknown++;

      // Count iPhone generations
      if (isIPhone) {
        if (model.includes('iphone 17')) counts.generations['17']++;
        else if (model.includes('iphone 16')) counts.generations['16']++;
        else if (model.includes('iphone 15')) counts.generations['15']++;
        else if (model.includes('iphone 14')) counts.generations['14']++;
        else if (model.includes('iphone 13') || model.includes('iphone 12') ||
                 model.includes('iphone 11') || model.includes('iphone x') ||
                 model.includes('iphone se') || model.includes('iphone 8')) counts.generations['Older']++;
        else counts.generations['Unknown']++;
      }
    });

    return counts;
  };

  const counts = getFilterCounts();

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontSize: '24px',
        fontFamily: 'Arial, sans-serif'
      }}>
        Loading data...
      </div>
    );
  }

  if (filteredData.length === 0) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontSize: '24px',
        fontFamily: 'Arial, sans-serif'
      }}>
        No data available with current filters
      </div>
    );
  }

  const headers = Object.keys(filteredData[0]);

  return (
    <div style={{
      padding: '20px',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1 style={{
        textAlign: 'center',
        marginBottom: '30px'
      }}>
        Facebook Marketplace Listings ({filteredData.length} of {data.length} items)
      </h1>

      {/* Device Type Filters */}
      <div style={{
        marginBottom: '20px',
        padding: '15px',
        backgroundColor: '#f8f9fa',
        borderRadius: '8px',
        border: '1px solid #dee2e6'
      }}>
        <div style={{
          fontSize: '16px',
          fontWeight: 'bold',
          marginBottom: '10px'
        }}>
          Device Type:
        </div>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          {Object.entries(deviceFilters).map(([filter, isActive]) => (
            <button
              key={filter}
              onClick={() => toggleDeviceFilter(filter)}
              style={{
                padding: '8px 16px',
                border: '2px solid',
                borderRadius: '20px',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: '500',
                backgroundColor: isActive ? '#007bff' : '#ffffff',
                color: isActive ? '#ffffff' : '#007bff',
                borderColor: '#007bff',
                transition: 'all 0.2s ease'
              }}
              onMouseOver={(e) => {
                if (!isActive) {
                  e.target.style.backgroundColor = '#e7f3ff';
                }
              }}
              onMouseOut={(e) => {
                if (!isActive) {
                  e.target.style.backgroundColor = '#ffffff';
                }
              }}
            >
              {filter.charAt(0).toUpperCase() + filter.slice(1)} ({counts.device[filter]})
            </button>
          ))}
        </div>
      </div>

      {/* iPhone Generation Filters */}
      {deviceFilters.iPhone && (
        <div style={{
          marginBottom: '20px',
          padding: '15px',
          backgroundColor: '#f8f9fa',
          borderRadius: '8px',
          border: '1px solid #dee2e6'
        }}>
          <div style={{
            fontSize: '16px',
            fontWeight: 'bold',
            marginBottom: '10px'
          }}>
            iPhone Generations:
          </div>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            {Object.entries(iphoneGenerationFilters).map(([filter, isActive]) => (
              <button
                key={filter}
                onClick={() => toggleIphoneGenerationFilter(filter)}
                style={{
                  padding: '8px 16px',
                  border: '2px solid',
                  borderRadius: '20px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  backgroundColor: isActive ? '#28a745' : '#ffffff',
                  color: isActive ? '#ffffff' : '#28a745',
                  borderColor: '#28a745',
                  transition: 'all 0.2s ease'
                }}
                onMouseOver={(e) => {
                  if (!isActive) {
                    e.target.style.backgroundColor = '#e8f5e8';
                  }
                }}
                onMouseOut={(e) => {
                  if (!isActive) {
                    e.target.style.backgroundColor = '#ffffff';
                  }
                }}
              >
                {filter === 'Older' ? '13 & Older' : filter} ({counts.generations[filter]})
              </button>
            ))}
          </div>
        </div>
      )}

      <div style={{
        overflowX: 'auto',
        maxWidth: '100vw'
      }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          border: '1px solid #ddd',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <thead>
            <tr style={{
              backgroundColor: '#f8f9fa',
              borderBottom: '2px solid #dee2e6'
            }}>
              {headers.map(header => {
                const isPriceColumn = header.toLowerCase() === 'price';
                let sortIndicator = '';
                if (isPriceColumn && sortByPrice === 'asc') sortIndicator = ' ↑';
                else if (isPriceColumn && sortByPrice === 'desc') sortIndicator = ' ↓';

                return (
                  <th
                    key={header}
                    onClick={isPriceColumn ? handlePriceSort : undefined}
                    style={{
                      padding: '12px',
                      textAlign: 'left',
                      fontWeight: 'bold',
                      border: '1px solid #ddd',
                      backgroundColor: isPriceColumn && sortByPrice !== 'none' ? '#28a745' : '#007bff',
                      color: 'white',
                      cursor: isPriceColumn ? 'pointer' : 'default'
                    }}
                  >
                    {header.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}{sortIndicator}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody>
            {filteredData.filter(row => Object.values(row).some(val => val && val.trim() !== '')).map((row, index) => (
              <tr key={index} style={{
                backgroundColor: index % 2 === 0 ? '#ffffff' : '#f8f9fa'
              }}>
                {headers.map(header => (
                  <td key={header} style={{
                    padding: '10px 12px',
                    border: '1px solid #ddd',
                    textAlign: 'left',
                    verticalAlign: 'middle'
                  }}>
                    {renderCellContent(row[header])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;