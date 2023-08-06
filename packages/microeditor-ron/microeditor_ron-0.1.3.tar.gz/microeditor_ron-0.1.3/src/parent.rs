use bevy_ecs::component::Component;
use bevy_ecs::entity::Entity;
use bevy_reflect::{Reflect, TypeRegistry};
use bevy_reflect::serde::ReflectSerializer;
use pyo3::prelude::*;

/// Temporary use local copy of Parent.
/// The bevy_hierarchy::components::Parent is private by the module
#[derive(Component, Debug, Eq, PartialEq, Reflect)]
pub struct Parent(pub(crate) Entity);

#[pyfunction]
pub fn parent(id: u32) -> PyResult<String> {
    let mut type_registry = TypeRegistry::default();
    type_registry.register::<Entity>();

    let value = Parent(Entity::from_raw(id));

    let serializer = ReflectSerializer::new(&value, &type_registry);
    let ron_string =
        ron::ser::to_string_pretty(&serializer, ron::ser::PrettyConfig::default()).unwrap();
    Ok(ron_string.replace("microeditor_ron::parent::Parent", "bevy_hierarchy::components::Parent"))
}

#[cfg(test)]
mod tests {
    use bevy_reflect::FromReflect;
    use bevy_reflect::serde::UntypedReflectDeserializer;
    use serde::de::DeserializeSeed;
    use super::*;

    #[test]
    fn test_parent_ron() {
        let result = parent(42);
        let result = ron_parent(result.unwrap());
        assert_eq!(42, result.get().index());
    }

    fn ron_parent(input: String) -> bevy_hierarchy::Parent {
        let mut type_registry = TypeRegistry::default();
        type_registry.register::<Entity>();

        let reflect_deserializer = UntypedReflectDeserializer::new(&type_registry);
        let mut ron_deserializer = ron::de::Deserializer::from_str(input.as_str()).unwrap();

        let dynamic_output = reflect_deserializer
            .deserialize(&mut ron_deserializer)
            .unwrap();

        let output = <bevy_hierarchy::Parent as FromReflect>::from_reflect(dynamic_output.as_ref()).unwrap();
        output
    }
}
