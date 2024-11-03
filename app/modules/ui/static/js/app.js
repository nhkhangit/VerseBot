// app/modules/ui/static/js/app.js
const { useState, useEffect } = React;
const IconPlus = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <line x1="12" y1="5" x2="12" y2="19"></line>
    <line x1="5" y1="12" x2="19" y2="12"></line>
  </svg>
);

const IconEdit = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
  </svg>
);

const IconTrash = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="16"
    height="16"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <polyline points="3 6 5 6 21 6"></polyline>
    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
  </svg>
);

// ... rest of the code
// API Service
const API = {
  // Projects
  async getProjects(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`/api/v1/projects?${params}`);
    return response.json();
  },

  async createProject(project) {
    const response = await fetch("/api/v1/projects/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(project),
    });
    return response.json();
  },

  async updateProject(id, project) {
    const response = await fetch(`/api/v1/projects/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(project),
    });
    return response.json();
  },

  async deleteProject(id) {
    await fetch(`/api/v1/projects/${id}`, { method: "DELETE" });
  },

  async changeProjectStatus(id, status) {
    const response = await fetch(`/api/v1/projects/${id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    return response.json();
  },

  // Tasks
  async getTasks(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`/api/v1/tasks?${params}`);
    return response.json();
  },

  async createTask(task) {
    const response = await fetch("/api/v1/tasks/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(task),
    });
    return response.json();
  },

  async updateTask(id, task) {
    const response = await fetch(`/api/v1/tasks/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(task),
    });
    return response.json();
  },

  async deleteTask(id) {
    await fetch(`/api/v1/tasks/${id}`, { method: "DELETE" });
  },

  async changeTaskStatus(id, status) {
    const response = await fetch(
      `/api/v1/tasks/${id}/status?status=${status}`,
      {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
      }
    );
    return response.json();
  },
};

// Components
const ProjectModal = ({ isOpen, onClose, onSubmit, project = null }) => {
  const [formData, setFormData] = useState(
    project || {
      name: "",
      description: "",
      start_date: "",
      end_date: "",
      status: "planning",
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg w-96">
        <h2 className="text-xl font-bold mb-4">
          {project ? "Edit Project" : "New Project"}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-2">Name</label>
            <input
              type="text"
              className="w-full border p-2 rounded"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2">Description</label>
            <textarea
              className="w-full border p-2 rounded"
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2">Start Date</label>
            <input
              type="datetime-local"
              className="w-full border p-2 rounded"
              value={formData.start_date}
              onChange={(e) =>
                setFormData({ ...formData, start_date: e.target.value })
              }
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2">End Date</label>
            <input
              type="datetime-local"
              className="w-full border p-2 rounded"
              value={formData.end_date}
              onChange={(e) =>
                setFormData({ ...formData, end_date: e.target.value })
              }
            />
          </div>
          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border rounded"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Sửa lại TaskModal
const TaskModal = ({
  isOpen,
  onClose,
  onSubmit,
  task = null,
  projectId = null, // ProjectId được truyền từ project đã chọn
}) => {
  const [formData, setFormData] = useState(
    task || {
      title: "",
      description: "",
      assignee: "",
      start_date: "",
      end_date: "",
      priority: 3,
      project_id: projectId, // Gán project_id vào form data
      status: "pending",
    }
  );

  // Reset form data khi modal mở ra với project id mới
  useEffect(() => {
    if (isOpen && !task) {
      setFormData((prev) => ({
        ...prev,
        project_id: projectId,
      }));
    }
  }, [isOpen, projectId, task]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      ...formData,
      project_id: projectId, // Đảm bảo project_id được gửi đi
    });
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg w-96">
        <h2 className="text-xl font-bold mb-4">
          {task ? "Edit Task" : "New Task"}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-2">Title</label>
            <input
              type="text"
              className="w-full border p-2 rounded"
              value={formData.title}
              onChange={(e) =>
                setFormData({ ...formData, title: e.target.value })
              }
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2">Description</label>
            <textarea
              className="w-full border p-2 rounded"
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2">Assignee</label>
            <input
              type="text"
              className="w-full border p-2 rounded"
              value={formData.assignee}
              onChange={(e) =>
                setFormData({ ...formData, assignee: e.target.value })
              }
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2">Priority (1-5)</label>
            <input
              type="number"
              min="1"
              max="5"
              className="w-full border p-2 rounded"
              value={formData.priority}
              onChange={(e) =>
                setFormData({ ...formData, priority: parseInt(e.target.value) })
              }
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2">Start Date</label>
            <input
              type="date"
              className="w-full border p-2 rounded"
              value={formData.start_date}
              onChange={(e) =>
                setFormData({ ...formData, start_date: e.target.value })
              }
              required
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2">End Date</label>
            <input
              type="date"
              className="w-full border p-2 rounded"
              value={formData.end_date}
              onChange={(e) =>
                setFormData({ ...formData, end_date: e.target.value })
              }
              required
            />
          </div>
          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border rounded"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Main App Component
const App = () => {
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Modals state
  const [isProjectModalOpen, setProjectModalOpen] = useState(false);
  const [isTaskModalOpen, setTaskModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [editingTask, setEditingTask] = useState(null);

  // Load projects
  useEffect(() => {
    loadProjects();
  }, []);

  // Load tasks when project selected
  useEffect(() => {
    if (selectedProject) {
      loadTasks(selectedProject.id);
    }
  }, [selectedProject]);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const data = await API.getProjects();
      setProjects(data.items || []);
    } catch (err) {
      setError("Failed to load projects");
    } finally {
      setLoading(false);
    }
  };

  const loadTasks = async (projectId) => {
    try {
      setLoading(true);
      const data = await API.getTasks({ project_id: projectId });
      setTasks(data.tasks || []);
    } catch (err) {
      setError("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  // Project handlers
  const handleCreateProject = async (project) => {
    try {
      await API.createProject(project);
      loadProjects();
    } catch (err) {
      setError("Failed to create project");
    }
  };

  const handleUpdateProject = async (id, project) => {
    try {
      await API.updateProject(id, project);
      loadProjects();
    } catch (err) {
      setError("Failed to update project");
    }
  };

  const handleDeleteProject = async (id) => {
    if (window.confirm("Are you sure you want to delete this project?")) {
      try {
        await API.deleteProject(id);
        loadProjects();
        if (selectedProject && selectedProject.id === id) {
          setSelectedProject(null);
        }
      } catch (err) {
        setError("Failed to delete project");
      }
    }
  };

  // Trong App component, sửa lại phần xử lý tạo task
  const handleCreateTask = async (task) => {
    try {
      if (!selectedProject) {
        setError("Please select a project first");
        return;
      }
      const taskWithProject = {
        ...task,
        project_id: selectedProject.id
      };
      await API.createTask(taskWithProject);
      loadTasks(selectedProject.id);
    } catch (err) {
      setError("Failed to create task");
    }
  };

  const handleUpdateTask = async (id, task) => {
    try {
      await API.updateTask(id, task);
      loadTasks(selectedProject.id);
    } catch (err) {
      setError("Failed to update task");
    }
  };

  const handleDeleteTask = async (id) => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      try {
        await API.deleteTask(id);
        loadTasks(selectedProject.id);
      } catch (err) {
        setError("Failed to delete task");
      }
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <button
        onClick={() => setProjectModalOpen(true)}
        className="px-4 py-2 bg-blue-500 text-white rounded flex items-center"
      >
        <IconPlus />
        <span className="ml-2">New Project</span>
      </button>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Main content */}
      <div className="grid grid-cols-12 gap-8">
        {/* Projects list */}
        <div className="col-span-4">
          <h2 className="text-xl font-semibold mb-4">Projects</h2>
          {loading ? (
            <div>Loading...</div>
          ) : (
            <div className="space-y-4">
              {projects.map((project) => (
                <div
                key={project.id}
                className={`p-4 rounded-lg border ${
                  selectedProject && selectedProject.id === project.id
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200"
                } cursor-pointer hover:border-blue-300`}
                onClick={() => setSelectedProject(project)}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-medium">{project.name}</h3>
                      <p className="text-sm text-gray-600">
                        {project.description}
                      </p>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation(); // Ngăn việc chọn project khi click vào nút edit
                          setEditingProject(project);
                          setProjectModalOpen(true);
                        }}
                        className="p-1 text-blue-600 hover:bg-blue-50 rounded"
                      >
                        <IconEdit />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation(); // Ngăn việc chọn project khi click vào nút delete
                          handleDeleteProject(project.id);
                        }}
                        className="p-1 text-red-600 hover:bg-red-50 rounded"
                      >
                        <IconTrash />
                      </button>
                    </div>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span
                      className={`px-2 py-1 rounded-full ${getStatusColor(
                        project.status
                      )}`}
                    >
                      {project.status}
                    </span>
                    <span className="text-gray-500">
                      Tasks:{" "}
                      {project.statistics ? project.statistics.total_tasks : 0}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Tasks list */}
        <div className="col-span-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">
              {selectedProject ? `Tasks - ${selectedProject.name}` : "Tasks"}
            </h2>
            {selectedProject && (
  <button
    onClick={() => setTaskModalOpen(true)}
    className="px-4 py-2 bg-green-500 text-white rounded flex items-center"
  >
    <IconPlus />
    <span className="ml-2">New Task</span>
  </button>
)}
          </div>

          {!selectedProject ? (
            <div className="text-center py-8 text-gray-500">
              Select a project to view tasks
            </div>
          ) : loading ? (
            <div>Loading...</div>
          ) : (
            <div className="space-y-4">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className="p-4 rounded-lg border border-gray-200"
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-medium">{task.title}</h3>
                      <p className="text-sm text-gray-600">
                        {task.description}
                      </p>
                    </div>
                    <div className="flex space-x-2">
                      <select
                        value={task.status}
                        onChange={(e) =>
                          API.changeTaskStatus(task.id, e.target.value).then(
                            () => loadTasks(selectedProject.id)
                          )
                        }
                        className="text-sm border rounded px-2 py-1"
                      >
                        <option value="pending">Pending</option>
                        <option value="in_progress">In Progress</option>
                        <option value="completed">Completed</option>
                      </select>
                      <button
                        onClick={() => {
                          setEditingTask(task);
                          setTaskModalOpen(true);
                        }}
                        className="p-1 text-blue-600 hover:bg-blue-50 rounded"
                      >
                        <IconEdit />
                      </button>
                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="p-1 text-red-600 hover:bg-red-50 rounded"
                      >
                        <IconTrash />
                      </button>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4 mt-2 text-sm">
                    <div>
                      <span className="text-gray-500">Assignee:</span>
                      <span className="ml-2">{task.assignee}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Priority:</span>
                      <span
                        className={`ml-2 px-2 py-1 rounded-full ${getPriorityColor(
                          task.priority
                        )}`}
                      >
                        P{task.priority}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Status:</span>
                      <span
                        className={`ml-2 px-2 py-1 rounded-full ${getStatusColor(
                          task.status
                        )}`}
                      >
                        {task.status}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Due:</span>
                      <span className="ml-2">
                        {new Date(task.end_date).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      <ProjectModal
        isOpen={isProjectModalOpen}
        onClose={() => {
          setProjectModalOpen(false);
          setEditingProject(null);
        }}
        onSubmit={(project) => {
          if (editingProject) {
            handleUpdateProject(editingProject.id, project);
          } else {
            handleCreateProject(project);
          }
        }}
        project={editingProject}
      />

<TaskModal
  isOpen={isTaskModalOpen}
  onClose={() => {
    setTaskModalOpen(false);
    setEditingTask(null);
  }}
  onSubmit={(task) => {
    if (editingTask) {
      handleUpdateTask(editingTask.id, task);
    } else {
      handleCreateTask(task);
    }
  }}
  task={editingTask}
  projectId={selectedProject ? selectedProject.id : null}
/>
    </div>
  );
};

// Utility functions
const getStatusColor = (status) => {
  const colors = {
    planning: "bg-blue-100 text-blue-800",
    active: "bg-green-100 text-green-800",
    on_hold: "bg-yellow-100 text-yellow-800",
    completed: "bg-purple-100 text-purple-800",
    cancelled: "bg-red-100 text-red-800",
    pending: "bg-gray-100 text-gray-800",
    in_progress: "bg-yellow-100 text-yellow-800",
  };
  return colors[status] || "bg-gray-100 text-gray-800";
};

const getPriorityColor = (priority) => {
  const colors = {
    1: "bg-gray-100 text-gray-800",
    2: "bg-green-100 text-green-800",
    3: "bg-yellow-100 text-yellow-800",
    4: "bg-orange-100 text-orange-800",
    5: "bg-red-100 text-red-800",
  };
  return colors[priority] || "bg-gray-100 text-gray-800";
};
// Task components
const TaskList = ({ projectId, onTaskUpdate }) => {
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (projectId) {
      loadTasks();
    }
  }, [projectId]);

  const loadTasks = async () => {
    try {
      setIsLoading(true);
      const data = await API.getTasks({ project_id: projectId });
      setTasks(data.tasks || []);
    } catch (error) {
      setError("Error loading tasks");
      console.error("Error loading tasks:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddTask = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleDeleteTask = async (taskId) => {
    if (confirm("Are you sure you want to delete this task?")) {
      try {
        await API.deleteTask(taskId);
        await loadTasks();
        if (onTaskUpdate) onTaskUpdate();
      } catch (error) {
        setError("Error deleting task");
        console.error("Error deleting task:", error);
      }
    }
  };

  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await API.changeTaskStatus(taskId, newStatus);
      await loadTasks();
      if (onTaskUpdate) onTaskUpdate();
    } catch (error) {
      setError("Error updating task status");
      console.error("Error updating task status:", error);
    }
  };

  return (
    <div className="space-y-4">
      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Add Task Button */}
      <div className="flex justify-end">
        <button
          onClick={handleAddTask}
          className="px-4 py-2 bg-blue-500 text-white rounded flex items-center"
        >
          <IconPlus />
          <span className="ml-2">Add Task</span>
        </button>
      </div>

      {/* Tasks list */}
      <div className="col-span-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">
            {selectedProject ? `Tasks - ${selectedProject.name}` : "Tasks"}
          </h2>
        </div>

        {!selectedProject ? (
          <div className="text-center py-8 text-gray-500">
            Select a project to view tasks
          </div>
        ) : (
          <TaskList
            projectId={selectedProject.id}
            onTaskUpdate={() => loadTasks(selectedProject.id)}
          />
        )}
      </div>

      {/* Task Modal */}
      <TaskModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingTask(null);
        }}
        task={editingTask}
        projectId={projectId}
        onSubmit={async (taskData) => {
          try {
            if (editingTask) {
              await API.updateTask(editingTask.id, taskData);
            } else {
              await API.createTask({
                ...taskData,
                project_id: projectId,
              });
            }
            await loadTasks();
            if (onTaskUpdate) onTaskUpdate();
            setIsModalOpen(false);
          } catch (error) {
            setError("Error saving task");
            console.error("Error saving task:", error);
          }
        }}
      />
    </div>
  );
};
// Cập nhật lại phần ProjectCard để hiển thị TaskList
const ProjectCard = ({ project, onEdit, onDelete }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="border rounded-lg">
      <div className="p-4">
        <div className="flex justify-between items-start">
          <div
            className="flex-1 cursor-pointer"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            <h3 className="font-medium">{project.name}</h3>
            <p className="text-sm text-gray-600">{project.description}</p>
          </div>
          <div className="flex space-x-2">
            <button onClick={onEdit}>
              <IconEdit />
            </button>
            <button onClick={onDelete}>
              <IconTrash />
            </button>
          </div>
        </div>
        <div className="mt-2 flex justify-between text-sm">
          <span
            className={`px-2 py-1 rounded-full ${getStatusColor(
              project.status
            )}`}
          >
            {project.status}
          </span>
          <span className="text-gray-500">
            Tasks: {project.statistics ? project.statistics.total_tasks : 0}
          </span>
        </div>
      </div>

      {isExpanded && (
        <div className="border-t p-4">
          <TaskList projectId={project.id} />
        </div>
      )}
    </div>
  );
};
// Render the app
// Thay vì dùng createRoot (React 18)
ReactDOM.render(<App />, document.getElementById("root"));
