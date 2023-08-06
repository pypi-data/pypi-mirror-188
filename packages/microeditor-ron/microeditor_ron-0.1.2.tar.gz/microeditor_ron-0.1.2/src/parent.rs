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
    use super::*;

    #[test]
    fn test_parent_ron() {
        let result = parent(42);
        println!("{}", result.unwrap());
    }
}
