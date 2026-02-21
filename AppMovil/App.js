import React, { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  TextInput, 
  TouchableOpacity, 
  FlatList, 
  Keyboard 
} from 'react-native';

export default function App() {
  const [nombre, setNombre] = useState('');
  const [compañeros, setCompañeros] = useState([]);

  
  const agregarCompañero = () => {
    if (nombre.trim().length > 0) {
      setCompañeros([...compañeros, { id: Date.now().toString(), name: nombre }]);
      setNombre(''); 
      Keyboard.dismiss();
    }
  };

  // Función para eliminar
  const eliminarCompañero = (id) => {
    setCompañeros(compañeros.filter(item => item.id !== id));
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Lista de Usuario</Text>
      
      <View style={styles.inputContainer}>
        <TextInput 
          style={styles.input}
          placeholder="Escribe un nombre..."
          value={nombre}
          onChangeText={setNombre}
        />
        <TouchableOpacity style={styles.button} onPress={agregarCompañero}>
          <Text style={styles.buttonText}>Agregar</Text>
        </TouchableOpacity>
      </View>

      <FlatList 
        data={compañeros}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text>{item.name}</Text>
            <TouchableOpacity onPress={() => eliminarCompañero(item.id)}>
              <Text style={styles.deleteText}>Eliminar</Text>
            </TouchableOpacity>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingTop: 60, paddingHorizontal: 20, backgroundColor: '#f5f5f5' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  inputContainer: { flexDirection: 'row', marginBottom: 20 },
  input: { flex: 1, borderWidth: 1, borderColor: '#ccc', padding: 10, borderRadius: 5, backgroundColor: '#fff' },
  button: { backgroundColor: '#007AFF', padding: 10, marginLeft: 10, borderRadius: 5, justifyContent: 'center' },
  buttonText: { color: 'white', fontWeight: 'bold' },
  item: { 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    padding: 15, 
    backgroundColor: '#fff', 
    borderRadius: 5, 
    marginBottom: 10,
    elevation: 2 // Sombra en Android
  },
  deleteText: { color: 'red', fontWeight: 'bold' }
});
