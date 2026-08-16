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
import { CourierPriorityItem } from "./CourierPriorityItem";

export interface CourierPriorityListProps {
  couriers: string[];
  courierStats?: Record<string, number>;
  onOrderChange: (newCouriers: string[]) => void;
}

export function CourierPriorityList({
  couriers,
  courierStats = {},
  onOrderChange,
}: CourierPriorityListProps) {
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
      const oldIndex = couriers.indexOf(String(active.id));
      const newIndex = couriers.indexOf(String(over.id));

      if (oldIndex !== -1 && newIndex !== -1) {
        onOrderChange(arrayMove(couriers, oldIndex, newIndex));
      }
    }
  };

  const moveCourier = (fromIndex: number, toIndex: number) => {
    if (toIndex >= 0 && toIndex < couriers.length) {
      onOrderChange(arrayMove(couriers, fromIndex, toIndex));
    }
  };

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <SortableContext items={couriers} strategy={verticalListSortingStrategy}>
        <div className="space-y-2.5">
          {couriers.map((courier, index) => (
            <CourierPriorityItem
              key={courier}
              id={courier}
              courierName={courier}
              labelCount={courierStats[courier]}
              priorityRank={index + 1}
              totalCouriers={couriers.length}
              canMoveUp={index > 0}
              canMoveDown={index < couriers.length - 1}
              onMoveUp={() => moveCourier(index, index - 1)}
              onMoveDown={() => moveCourier(index, index + 1)}
            />
          ))}
        </div>
      </SortableContext>
    </DndContext>
  );
}
