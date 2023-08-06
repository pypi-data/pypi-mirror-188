use bevy_reflect::{DynamicTupleStruct, Reflect, TypeRegistry};
use bevy_reflect::serde::ReflectSerializer;
use bevy_transform::components::GlobalTransform;
use glam::Mat4;
use pyo3::prelude::*;

use crate::transform::{Quaternion, Vector};

#[pyfunction]
pub fn global_transform(
    translation: Vector,
    rotation: Quaternion,
    scale: Vector,
) -> PyResult<String> {
    let mut type_registry = TypeRegistry::default();
    type_registry.register::<GlobalTransform>();

    let mat4 = Mat4::from_scale_rotation_translation(
        scale.to_vec3(),
        rotation.to_quat(),
        translation.to_vec3(),
    );

    let mut value = GlobalTransform::from(mat4);

    let patch = DynamicTupleStruct::default();
    value.apply(&patch);

    let serializer = ReflectSerializer::new(&value, &type_registry);
    let ron_string =
        ron::ser::to_string_pretty(&serializer, ron::ser::PrettyConfig::default()).unwrap();
    Ok(ron_string)
}


#[cfg(test)]
mod tests {
    use bevy_reflect::FromReflect;
    use bevy_reflect::serde::UntypedReflectDeserializer;
    use glam::{Affine3A, Mat3A, Vec3A};
    use serde::de::DeserializeSeed;

    use super::*;

    #[test]
    fn serialize_deserialize_transform() {
        let translation = Vector(5.0, 2.0, 3.0);
        let rotation = Quaternion(1.0, 1.0, 1.0, 1.0);
        let scale = Vector(1.0, 1.0, 1.0);
        let ron_string = global_transform(translation, rotation, scale);
        let ron_string = ron_string.unwrap();
        let global_transform = ron_global_transform(ron_string);
        assert_eq!(global_transform.translation().x, 5.0);
        assert_eq!(global_transform.translation().y, 2.0);
        assert_eq!(global_transform.translation().z, 3.0);
    }

    // You fucking deleted ron_transform!!!
    fn ron_global_transform(input: String) -> GlobalTransform {
        let mut type_registry = TypeRegistry::default();
        type_registry.register::<GlobalTransform>();
        type_registry.register::<Affine3A>();
        type_registry.register::<Mat3A>();
        type_registry.register::<Vec3A>();

        let reflect_deserializer = UntypedReflectDeserializer::new(&type_registry);
        let mut ron_deserializer = ron::de::Deserializer::from_str(input.as_str()).unwrap();

        let dynamic_output = reflect_deserializer
            .deserialize(&mut ron_deserializer)
            .unwrap();
        let output = <GlobalTransform as FromReflect>::from_reflect(dynamic_output.as_ref()).unwrap();
        output
    }
}
