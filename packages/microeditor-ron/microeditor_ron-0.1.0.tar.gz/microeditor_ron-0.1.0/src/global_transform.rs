use crate::transform::{Quaternion, Vector};
use bevy_reflect::serde::ReflectSerializer;
use bevy_reflect::{DynamicStruct, Reflect, TypeRegistry};
use bevy_transform::components::GlobalTransform;
use glam::{Mat4, Quat};
use pyo3::prelude::*;

#[pyfunction]
pub fn global_transform(
    translation: Vector,
    rotation: Quaternion,
    scale: Vector,
) -> PyResult<String> {
    let mut type_registry = TypeRegistry::default();
    type_registry.register::<Quat>();

    let mat4 = Mat4::from_scale_rotation_translation(
        scale.to_vec3(),
        rotation.to_quat(),
        translation.to_vec3(),
    );

    let mut value = GlobalTransform::from(mat4);

    let patch = DynamicStruct::default();
    value.apply(&patch);

    let serializer = ReflectSerializer::new(&value, &type_registry);
    let ron_string =
        ron::ser::to_string_pretty(&serializer, ron::ser::PrettyConfig::default()).unwrap();
    Ok(ron_string)
}
