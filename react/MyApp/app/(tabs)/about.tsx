import { styles } from '../../assets/my_styles';

import EditScreenInfo from "@/components/EditScreenInfo";
import { Text, View } from "@/components/Themed";


export default function AboutScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>about</Text>
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <EditScreenInfo path="app/(tabs)/about.tsx" />
    </View>
  );
}

