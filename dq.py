try {
    method.invoke(obj, args);
} catch (InvocationTargetException e) {
    throw new RuntimeException("Error during method invocation", e.getCause());
}
