import { Image } from 'react-native';
import { styles } from '../../assets/my_styles';

import EditScreenInfo from '@/components/EditScreenInfo';
import { Text, View } from '@/components/Themed';

const image = require('../assets/images/Boston_University_Terriers_logo.svg');

export default function IndexScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Index</Text>
      <Text>This is the main page and an example of text being displayed as well as an image!</Text>
      <Image source={image} style={{ width: 100, height: 100 }} />
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <EditScreenInfo path="app/(tabs)/index.tsx" />
    </View>
  );
}


