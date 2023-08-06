use bevy_reflect::serde::ReflectSerializer;
use bevy_reflect::{DynamicStruct, Reflect, TypeRegistry};
use bevy_transform::components::Transform;
use glam::{Quat, Vec3};
use pyo3::prelude::*;

/// <Vector (0, 1, 2)>
#[derive(FromPyObject)]
pub struct Vector(f32, f32, f32);

impl Vector {
    pub(crate) fn to_vec3(self) -> Vec3 {
        Vec3::new(self.0, self.1, self.2)
    }
}

/// <Quaternion (w=0, x=1, y=2, z=3)>
#[derive(FromPyObject)]
pub struct Quaternion(f32, f32, f32, f32);

impl Quaternion {
    pub(crate) fn to_quat(self) -> Quat {
        Quat::from_xyzw(self.1, self.2, self.3, self.0)
    }
}

/// Serializes transform into ron string.
#[pyfunction]
pub fn transform(translation: Vector, rotation: Quaternion, scale: Vector) -> PyResult<String> {
    let mut type_registry = TypeRegistry::default();
    type_registry.register::<Quat>();

    let mut value = Transform::from_translation(translation.to_vec3());
    value.rotation = rotation.to_quat();
    value.scale = scale.to_vec3();

    let patch = DynamicStruct::default();
    value.apply(&patch);

    let serializer = ReflectSerializer::new(&value, &type_registry);
    let ron_string =
        ron::ser::to_string_pretty(&serializer, ron::ser::PrettyConfig::default()).unwrap();
    Ok(ron_string)
}

#[cfg(test)]
mod tests {
    use super::*;
    use bevy_reflect::serde::UntypedReflectDeserializer;
    use bevy_reflect::FromReflect;
    use serde::de::DeserializeSeed;

    #[test]
    fn serialize_deserialize_transform() {
        let translation = Vector(5.0, 2.0, 3.0);
        let rotation = Quaternion(1.0, 1.0, 1.0, 1.0);
        let scale = Vector(1.0, 1.0, 1.0);
        let ron_string = transform(translation, rotation, scale);
        let ron_string = ron_string.unwrap();
        let transform = ron_transform(ron_string);
        assert_eq!(transform.translation.x, 5.0);
        assert_eq!(transform.translation.y, 2.0);
        assert_eq!(transform.translation.z, 3.0);
    }

    // You fucking deleted ron_transform!!!
    fn ron_transform(input: String) -> Transform {
        let mut type_registry = TypeRegistry::default();
        type_registry.register::<Quat>();
        type_registry.register::<Transform>();
        type_registry.register::<Vec3>();

        let reflect_deserializer = UntypedReflectDeserializer::new(&type_registry);
        let mut ron_deserializer = ron::de::Deserializer::from_str(input.as_str()).unwrap();

        let dynamic_output = reflect_deserializer
            .deserialize(&mut ron_deserializer)
            .unwrap();
        let output = <Transform as FromReflect>::from_reflect(dynamic_output.as_ref()).unwrap();
        output
    }
}
