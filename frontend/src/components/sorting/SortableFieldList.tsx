import React from "react";
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { SortableFieldItem } from "./SortableFieldItem";
import { SortableField } from "@/types";

export interface SortableFieldListProps {
  fields: SortableField[];
  selectedFieldIds: string[];
  onOrderChange: (newFields: SortableField[]) => void;
  onToggleField: (fieldId: string) => void;
}

export function SortableFieldList({
  fields,
  selectedFieldIds,
  onOrderChange,
  onToggleField,
}: SortableFieldListProps) {
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 5,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const oldIndex = fields.findIndex((f) => f.id === active.id);
      const newIndex = fields.findIndex((f) => f.id === over.id);

      if (oldIndex !== -1 && newIndex !== -1) {
        onOrderChange(arrayMove(fields, oldIndex, newIndex));
      }
    }
  };

  const moveField = (fromIndex: number, toIndex: number) => {
    if (toIndex >= 0 && toIndex < fields.length) {
      onOrderChange(arrayMove(fields, fromIndex, toIndex));
    }
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <SortableContext
        items={fields.map((f) => f.id)}
        strategy={verticalListSortingStrategy}
      >
        <div className="space-y-2.5">
          {fields.map((field, index) => {
            const isSelected = selectedFieldIds.includes(field.id);
            return (
              <SortableFieldItem
                key={field.id}
                id={field.id}
                label={field.label}
                uniqueValues={field.unique_values}
                totalLabels={field.total_labels}
                rank={index + 1}
                isSelected={isSelected}
                onToggleSelect={() => onToggleField(field.id)}
                canMoveUp={index > 0}
                canMoveDown={index < fields.length - 1}
                onMoveUp={() => moveField(index, index - 1)}
                onMoveDown={() => moveField(index, index + 1)}
              />
            );
          })}
        </div>
      </SortableContext>
    </DndContext>
  );
}
